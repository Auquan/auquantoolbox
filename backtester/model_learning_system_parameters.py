import sys, os
import glob, json
import numpy as np
from dateutil import parser
from datetime import timedelta
from backtester.features.feature_config import FeatureConfig
from backtester.dataSource import data_source_classes
from backtester.dataSource.features_data_source import FeaturesDataSource
from backtester.feature_manager import FeatureManager
from backtester.constants import *
from backtester.logger import *


class ModelLearningSystemParamters(object):
    def __init__(self, symbols, targetVariable, chunkSize=None, models=None):
        self.instrumentIds = symbols
        self.chunkSize = chunkSize
        self.trainingDataSource = None
        self.validationDataSource = None
        self.testDataSource = None
        self.validationSplit = None
        self.targetVariable = None

        FeatureConfig.setupCustomFeatures(self.getCustomFeatures())
        self.__instrumentFeatureConfigs = {}

        instrumentFeatureConfigDicts = self.getInstrumentFeatureConfigDicts()
        for instrumentType in instrumentFeatureConfigDicts:
            if type(instrumentFeatureConfigDicts[instrumentType]) is list:
                self.__instrumentFeatureConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), instrumentFeatureConfigDicts[instrumentType]))
            elif type(instrumentFeatureConfigDicts[instrumentType]) is dict:
                self.__instrumentFeatureConfigs[instrumentType] = {k : FeatureConfig(v) for k, v in instrumentFeatureConfigDicts[instrumentType]}
            else:
                logError("Unknown type of instruments' feature config dicts")

        self.__targetVariableConfigs = {}
        targetVariableConfigDicts = self.getTargetVariableConfigDicts()
        for instrumentType in targetVariableConfigDicts:
            self.__targetVariableConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), targetVariableConfigDicts[instrumentType]))

    def initializeDataSource(self, dataSourceName, **params):
        dataSourceClass = getattr(data_source_classes, dataSourceName)
        cachedFolderName = params.get('cachedFolderName', '')
        dataSetId = params.get('dataSetId', '')
        startDateStr = params.get('startDateStr', None)
        endDateStr = params.get('endDateStr', None)
        featureFolderName = params.get('featureFolderName', 'features')
        # NOTE: Hardcoded name of json file
        stockDataFile = os.path.join(cachedFolderName, dataSetId, featureFolderName, 'stock_data.json')
        actionDict = self.checkFeaturesExistence(stockDataFile, startDateStr, endDateStr)
        # TODO: Also compute and check the hash of instrument feature files with the hash stored in json file
        if actionDict['exist']:
            logInfo("Features found!")
        elif actionDict['recalculate']:
            dataSource = dataSourceClass(**params)
            featureManager = FeatureManager(self, dataSource, self.instrumentIds, self.chunkSize)
            featureManager.computeInstrumentFeatures(self.instrumentIds, writeFeatures=True)
        else:
            self.fixFeaturesData(dataSourceClass, actionDict, params.copy())

        params['features'] = self.features
        self.trainingDataSource = FeaturesDataSource(**params)
        # self.validationDataSource = None
        # self.testDataSource = None

    def fixFeaturesData(self, dataSourceClass, actionDict, params):
        startDateStr = params.get('startDateStr', None)
        endDateStr = params.get('endDateStr', None)
        for dates in actionDict['dateRange']:
            instrumentIds = [inst for inst in self.instrumentIds if inst not in actionDict['instrumentIds']]
            print(instrumentIds)
            params['instrumentIds'] = instrumentIds
            params['startDateStr'] = dates['startDate']
            params['endDateStr'] = dates['endDate']
            dataSource = dataSourceClass(**params)
            featureManager = FeatureManager(self, dataSource, instrumentIds, self.chunkSize)
            featureManager.computeInstrumentFeatures(instrumentIds, writeFeatures=True, prepend=dates['prepend'], updateFingerprint=True)

        if len(actionDict['instrumentIds']) > 0:
            params['instrumentIds'] = actionDict['instrumentIds']
            params['startDateStr'] = startDateStr
            params['endDateStr'] = endDateStr
            dataSource = dataSourceClass(**params)
            featureManager = FeatureManager(self, dataSource, actionDict['instrumentIds'], self.chunkSize)
            featureManager.computeInstrumentFeatures(actionDict['instrumentIds'], writeFeatures=True, updateFingerprint=True)

    def checkFeaturesExistence(self, stockDataFile, startDateStr, endDateStr):
        instrumentFeatureConfigs = self.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        self.features = list(map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs))
        lookbackSize = FeatureManager.parseFeatureConfigs(instrumentFeatureConfigs) - 1
        actionDict = {'exist' : False, 'recalculate' : True, 'instrumentIds' : [], 'dateRange' : []}
        try:
            with open(stockDataFile, 'r') as fp:
                fingerprint = json.load(fp)
        except FileNotFoundError:
            logWarn('stock_data.json file not found')
            return actionDict
        if lookbackSize != fingerprint['lookbackSize']:
            return actionDict
        if not set(self.features).issubset(set(fingerprint['features'])):
            return actionDict
        existingInstrumentFiles = glob.glob(os.path.join(os.path.dirname(stockDataFile), '*.csv'))
        existingInstruments = [os.path.splitext(os.path.basename(instrumentFile))[0] for instrumentFile in existingInstrumentFiles]
        actionDict['instrumentIds'] = list(np.setdiff1d(self.instrumentIds,
                                           list(set(existingInstruments) & set(fingerprint['stocks']))))
        actionDict['recalculate'], actionDict['dateRange'] = self.checkFeaturesDates(fingerprint,
                                                                                     startDateStr, endDateStr)
        if len(actionDict['instrumentIds']) > 0 or len(actionDict['dateRange']) > 0 :
            return actionDict
        actionDict['exist'] = True
        actionDict['recalculate'] = False
        return actionDict

    def checkFeaturesDates(self, fingerprint, expStartDateStr, expEndDateStr):
        if expStartDateStr is None or expEndDateStr is None:
            raise ValueError
        expStartDate = parser.parse(expStartDateStr)
        expEndDate = parser.parse(expEndDateStr)
        orgStartDate = parser.parse(fingerprint['startDate'])
        orgEndDate = parser.parse(fingerprint['endDate'])
        periodStartDate = parser.parse(fingerprint['periodStartDate'])
        periodEndDate = parser.parse(fingerprint['periodEndDate'])
        cond1 = orgStartDate > expStartDate and orgEndDate < expEndDate
        cond2 = orgStartDate > expStartDate and orgEndDate >= expEndDate
        cond3 = orgStartDate <= expStartDate and orgEndDate < expEndDate
        cond4 = expStartDate > orgEndDate
        cond5 = expEndDate < orgStartDate
        topDateStr = (orgStartDate - timedelta(days=1)).strftime('%Y%m%d') if periodStartDate is None else fingerprint['periodStartDate']
        botDateStr = (orgEndDate + timedelta(days=1)).strftime('%Y%m%d') if periodEndDate is None else fingerprint['periodEndDate']
        if cond1:
            return False, [dict(startDate=expStartDateStr,
                                endDate=topDateStr,
                                prepend=True),
                           dict(startDate=botDateStr,
                                endDate=expEndDateStr,
                                prepend=False)]
        if (cond2 and cond5) or (cond3 and cond4):
            return True, [dict(startDate=expStartDateStr,
                               endDate=expEndDateStr,
                               prepend=False)]
        elif cond2:
            return False, [dict(startDate=expStartDateStr,
                                endDate=topDateStr,
                                prepend=True)]
        elif cond3:
            return False, [dict(startDate=botDateStr,
                                endDate=expEndDate.strftime('%Y%m%d'),
                                prepend=False)]
        else:
            return False, []

    def setTargetVariable(self):
        pass

    def setTrainingDataSource(self, dataSetId, dateRange):
        raise NotImplementedError
        return

    def setValidationDataSource(self, dataSetId, dateRange):
        raise NotImplementedError
        return

    def setTrainingDataSource(self, dataSetId, dateRange):
        raise NotImplementedError
        return

    def getInstrumentFeatureConfigDicts(self):
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'Open'}}

        return {INSTRUMENT_TYPE_STOCK: [ma2Dict]}

    def getCustomFeatures(self):
        return {}

    def getTargetVariableConfigDicts(self):
        tv_ma5 = {'featureKey' : 'tv_ma5',
                   'featureId' : 'moving_average',
                   'params' : {'period' : 5,
                               'featureName' : 'ma_5',
                               'shift' : 10}}
        return {INSTRUMENT_TYPE_STOCK: [tv_ma5]}

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__instrumentFeatureConfigs:
            return self.__instrumentFeatureConfigs[instrumentType]
        else:
            return []

    def getTargetVariableConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__targetVariableConfigs:
            return self.__targetVariableConfigs[instrumentType]
        else:
            return []

    def getTrainingDataSource(self):
        return self.trainingDataSource

    def getValidationDataSource(self):
        return self.validationDataSource

    def getTestDataSource(self):
        return self.testDataSource
