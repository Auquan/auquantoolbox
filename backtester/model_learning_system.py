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
        self.__targetVariable = mlsParams.getTargetVariable()
        self.__trainingDataSource = mlsParams.getTrainingDataSource()
        self.__chunkSize = mlsParams.chunkSize

    def getTrainingInstrurmentData(self, instrumentId, chunkSize=None):
        return self.__trainingDataSource.getInstrumentUpdates(instrumentId, chunkSize)

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
