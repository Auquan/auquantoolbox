import sys, os
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from backtester.model_learning_system_parameters import ModelLearningSystemParamters
from backtester.feature_manager import FeatureManager
from backtester.constants import *

class ModelLearningSystem:
    def __init__(self, mlsParams):
        self.mlsParams = mlsParams
        # self.__targetVariable = mlsParams.getTargetVariable()
        self.__trainingDataSource = mlsParams.getTrainingDataSource()
        self.__chunkSize = mlsParams.chunkSize
        self.__targetVariableManager = TargetVariableManager(mlsParams, instrumentIds=mlsParams.instrumentIds)

    def getTrainingInstrurmentData(self, instrumentId, chunkSize=None):
        return self.__trainingDataSource.getInstrumentUpdates(instrumentId, chunkSize)

    def getTargetVariables(self, targetVariableConfigs):
        targetVariableConfigs = targetVariableConfigs if isinstance(targetVariableConfigs, list) else [targetVariableConfigs]
        targetVariableKeys = map(lambda x: x.getFeatureKey(), targetVariableConfigs)
        targetVariable = {}
        for key in targetVariableKeys:
            targetVariable[key] = self.__targetVariableManager.getTargetVariableByKey(key)
        return targetVariable

    def computeTargetVariables(self, instrumentData, instrumentId, targetVariableConfigs, chunkSize=None):
        if chunkSize is None:
            self.__targetVariableManager.computeTargetVariables(0, instrumentData, instrumentId, targetVariableConfigs)
            targetVariable = self.getTargetVariables(targetVariableConfigs)
            print(targetVariable)

    def getFeatureSet(self):
        return self.mlsParams.features

    def findBestModel(self):
        pass

    def getFinalMetrics(self):
        pass

if __name__ == '__main__':
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2015/07/10'
    endDateStr = '2017/09/07'
    chunkSize = 1000
    mlsParams = ModelLearningSystemParamters(instrumentIds, 'XYZ', chunkSize=chunkSize)
    params = dict(cachedFolderName='yahooData/',
                 dataSetId='testTrading',
                 instrumentIds=instrumentIds,
                 startDateStr=startDateStr,
                 endDateStr=endDateStr,
                 liveUpdates=False)
    mlsParams.initializeDataSource('YahooStockDataSource', **params)

    # mlsParams.trainingDataSource = YahooStockDataSource()
    # print(mlsParams.trainingDataSource.emitAllInstrumentUpdates()['IBM'].getBookData())

    system1 = ModelLearningSystem(mlsParams)
    print(system1.getTrainingInstrurmentData('IBM').getBookData())
