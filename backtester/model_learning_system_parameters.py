import sys, os
import glob, json
import numpy as np
from dateutil import parser
from datetime import timedelta
from backtester.features.feature_config import FeatureConfig
from backtester.constants import *
from backtester.logger import *
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.dataSource.features_data_source import FeaturesDataSource
from backtester.feature_manager import FeatureManager


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

    def initializeDataSource(self, dataSourceName, **params):
        cachedFolderName = params.get('cachedFolderName', None)
        dataSetId = params.get('dataSetId', None)
        startDateStr = params.get('startDateStr', None)
        endDateStr = params.get('endDateStr', None)
        featureFolderName = params.get('featureFolderName', 'features')
        # NOTE: Hardcoded name of json file
        stockDataFile = os.path.join(cachedFolderName, dataSetId, featureFolderName, 'stock_data.json')
        actionDict = self.checkFeaturesExistence(stockDataFile, startDateStr, endDateStr)
        if actionDict['exist']:
            logInfo("Features found")
        elif actionDict['recalculate']:
            dataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                             dataSetId=dataSetId,
                                             instrumentIds=self.instrumentIds,
                                             startDateStr=startDateStr,
                                             endDateStr=endDateStr,
                                             event='history',
                                             liveUpdates=False)
            featureManager = FeatureManager(self, dataSource, self.instrumentIds, self.chunkSize)
            featureManager.computeInstrumentFeatures(self.instrumentIds, writeFeatures=True)
        else:
            self.fixFeaturesData(dataSourceName, actionDict, params)

        self.trainingDataSource = FeaturesDataSource(cachedFolderName=cachedFolderName,
                                                     dataSetId=dataSetId,
                                                     instrumentIds=self.instrumentIds,
                                                     features=self.features,
                                                     startDateStr=startDateStr,
                                                     endDateStr=endDateStr,
                                                     featureFolderName=featureFolderName,
                                                     liveUpdates=False)
        # self.validationDataSource = None
        # self.testDataSource = None

        # handlerClass = getattr(urllib2, 'HTTPHandler')

    def fixFeaturesData(self, dataSourceName, actionDict, params):
        cachedFolderName = params.get('cachedFolderName', None)
        dataSetId = params.get('dataSetId', None)
        startDateStr = params.get('startDateStr', None)
        endDateStr = params.get('endDateStr', None)
        featureFolderName = params.get('featureFolderName', 'features')
        for dates in actionDict['dateRange']:
            dataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                             dataSetId=dataSetId,
                                             instrumentIds=self.instrumentIds,
                                             startDateStr=dates['startDate'],
                                             endDateStr=dates['endDate'],
                                             event='history',
                                             liveUpdates=False)
            instruments = [inst for inst in self.instrumentIds if inst not in actionDict['instrumentIds']]
            featureManager = FeatureManager(self, dataSource, instruments, self.chunkSize)
            featureManager.computeInstrumentFeatures(instruments, writeFeatures=True, prepend=dates['prepend'], updateFingerprint=True)

        if len(actionDict['instrumentIds']) > 0:
            dataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                             dataSetId=dataSetId,
                                             instrumentIds=actionDict['instrumentIds'],
                                             startDateStr=startDateStr,
                                             endDateStr=endDateStr,
                                             event='history',
                                             liveUpdates=False)
            featureManager = FeatureManager(self, dataSource, actionDict['instrumentIds'], self.chunkSize)
            featureManager.computeInstrumentFeatures(actionDict['instrumentIds'], writeFeatures=True, updateFingerprint=True)

    def checkFeaturesExistence(self, stockDataFile, startDateStr, endDateStr):
        instrumentFeatureConfigs = self.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        self.features = list(map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs))
        actionDict = {'exist' : False, 'recalculate' : True, 'instrumentIds' : [], 'dateRange' : []}
        try:
            with open(stockDataFile, 'r') as fp:
                fingerprint = json.load(fp)
        except FileNotFoundError:
            logWarn('stock_data.json file not found')
            return actionDict
        if not set(self.features).issubset(set(fingerprint['features'])):
            return actionDict
        existingInstrumentFiles = glob.glob(os.path.join(os.path.dirname(stockDataFile), '*.csv'))
        existingInstruments = [os.path.splitext(os.path.basename(instrumentFile))[0] for instrumentFile in existingInstrumentFiles]
        actionDict['instrumentIds'] = list(np.setdiff1d(self.instrumentIds,
                                           list(set(existingInstruments) & set(fingerprint['stocks']))))
        actionDict['recalculate'], actionDict['dateRange'] = self.checkFeaturesDates(fingerprint['startDate'],
                                                                                     fingerprint['endDate'],
                                                                                     startDateStr, endDateStr)
        if len(actionDict['instrumentIds']) > 0 or len(actionDict['dateRange']) > 0 :
            return actionDict
        actionDict['exist'] = True
        actionDict['recalculate'] = False
        return actionDict

    def checkFeaturesDates(self, orgStartDate, orgEndDate, expStartDate, expEndDate):
        expStartDate = parser.parse(expStartDate)
        expEndDate = parser.parse(expEndDate)
        orgStartDate = parser.parse(orgStartDate)
        orgEndDate = parser.parse(orgEndDate)
        cond1 = orgStartDate > expStartDate and orgEndDate < expEndDate
        cond2 = orgStartDate > expStartDate and orgEndDate > expEndDate
        cond3 = orgStartDate < expStartDate and orgEndDate < expEndDate
        cond4 = expStartDate > orgEndDate
        cond5 = expEndDate < orgStartDate
        if cond1:
            return False, [dict(startDate=expStartDate.strftime('%Y%m%d'),
                                endDate=(orgStartDate - timedelta(days=1)).strftime('%Y%m%d'),
                                prepend=True),
                           dict(startDate=(orgEndDate + timedelta(days=1)).strftime('%Y%m%d'),
                                endDate=expEndDate.strftime('%Y%m%d'),
                                prepend=False)]
        if (cond2 and cond5) or (cond3 and cond4):
            return True, [dict(startDate=expStartDate.strftime('%Y%m%d'),
                               endDate=expEndDate.strftime('%Y%m%d'),
                               prepend=False)]
        elif cond2:
            return False, [dict(startDate=expStartDate.strftime('%Y%m%d'),
                                endDate=(orgStartDate - timedelta(days=1)).strftime('%Y%m%d'),
                                prepend=True)]
        elif cond3:
            return False, [dict(startDate=(orgEndDate + timedelta(days=1)).strftime('%Y%m%d'),
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

    def getTargetVariable(self):
        pass

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__instrumentFeatureConfigs:
            return self.__instrumentFeatureConfigs[instrumentType]
        else:
            return []

    def getTrainingDataSource(self):
        return self.trainingDataSource

    def getValidationDataSource(self):
        return self.validationDataSource

    def getTestDataSource(self):
        return self.testDataSource
