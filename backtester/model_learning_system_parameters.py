import sys, os
from backtester.features.feature_config import FeatureConfig
from backtester.constants import *


class ModelLearningSystemParamters(object):
    def __init__(self, symbols, targetVariable, models=None):
        self.instrumentIds = symbols
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

    def initializeDataSource(self, dataSourceName, params):
        # NOTE: Hardcoded name of json file
        stockDataFile = os.path.join(cachedFolderName, dataSetId, featureFolderName, 'stock_data.json')
        actionDict = self.checkFeaturesExistence(stockDataFile, startDateStr, endDateStr)
        if actionDict['exist']:
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
        elif actionDict['recalculate']:
            self.trainingDataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                             dataSetId=dataSetId,
                                             instrumentIds=self.instrumentIds,
                                             startDateStr=startDateStr,
                                             endDateStr=endDateStr,
                                             event='history',
                                             liveUpdates=False)
        else:
            self.fixFeaturesData(dataSourceName, actionDict, params)

        # handlerClass = getattr(urllib2, 'HTTPHandler')

    def fixFeaturesData(self, dataSourceName, actionDict, params):
        for dates in actionDict['dateRange']:
            self.trainingDataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                             dataSetId=dataSetId,
                                             instrumentIds=self.instrumentIds,
                                             startDateStr=dates[0],
                                             endDateStr=dates[1],
                                             event='history',
                                             liveUpdates=False)
            # TODO: USE append
            featureManager = FeatureManager(self, self.trainingDataSource, self.chunkSize)
            instruments = [i if i not in actionDict['instrumentIds'] for i in self.instrumentIds]
            featureManager.computeInstrumentFeatures(instruments, writeFeatures=True)

        self.trainingDataSource = YahooStockDataSource(cachedFolderName=cachedFolderName,
                                         dataSetId=dataSetId,
                                         instrumentIds=actionDict['instrumentIds'],
                                         startDateStr=startDateStr,
                                         endDateStr=endDateStr,
                                         event='history',
                                         liveUpdates=False)
        featureManager = FeatureManager(self, self.trainingDataSource, self.chunkSize)
        featureManager.computeInstrumentFeatures(actionDict['instrumentIds'], writeFeatures=True)


    def checkFeaturesExistence(self, stockDataFile, startDateStr, endDateStr):
        instrumentFeatureConfigs = self.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        self.features = map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs)
        actionDict = {'exist' : False, 'recalculate' : True, 'instrumentIds' : [], 'dateRange' : []}
        try:
            with open(stockDataFile, 'r') as fp:
                fingerprint = json.load(fp)
        except FileNotFoundError:
            logWarn('stock_data.json file not found')
            return actionDict
        if not set(features).issubset(set(fingerprint['features'])):
            return actionDict
        actionDict['instrumentIds'] = np.setdiff1d(self.instrumentIds, fingerprint['stocks'])
        actionDict['recalculate'], actionDict['dateRange'] = self.checkFeaturesDates(fingerprint['startDate'],
                                                                                     fingerprint['endDate'],
                                                                                     startDateStr, endDateStr)
        if len(instrumentIds) > 0 or len(actionDict['dateRange']) > 0 :
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
                                append=False),
                           dict(startDate=(orgEndDate + timedelta(days=1)).strftime('%Y%m%d'),
                                endDate=expEndDate.strftime('%Y%m%d'),
                                append=True)]
        if (cond2 and cond5) or (cond3 and cond4):
            return True, [dict(startDate=expStartDate.strftime('%Y%m%d'),
                               endDate=expEndDate.strftime('%Y%m%d'),
                               append=False)]
        elif cond2:
            return False, [dict(startDate=expStartDate.strftime('%Y%m%d'),
                                endDate=(orgStartDate - timedelta(days=1)).strftime('%Y%m%d'),
                                append=False)]
        elif cond3:
            return False, [dict(startDate=(orgEndDate + timedelta(days=1)).strftime('%Y%m%d'),
                                endDate=expEndDate.strftime('%Y%m%d'),
                                append=True)]
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
