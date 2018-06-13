import sys, os
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from backtester.model_learning_system_parameters import ModelLearningSystemParamters
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.dataSource.features_data_source import FeaturesDataSource
from backtester.feature_manager import FeatureManager
from backtester.constants import *


class ModelLearningSystem:
    def __init__(self, mlsParams):
        self.mlsParams = mlsParams
        self.__targetVariable = mlsParams.getTargetVariable()
        self.__trainingDataSource = mlsParams.getTrainingDataSource()
        self.__chunkSize = mlsParams.chunkSize
        # self.__trainingFeatureManager = FeatureManager(self.mlsParams, self.__trainingDataSource, chunkSize)

    def getTrainingInstrurmentData(self, instrumentId, chunkSize=None):
        return self.__trainingDataSource.getInstrumentUpdates(instrumentId, chunkSize)

    def generateFeatures(self):
        self.__trainingFeatureManager.computeInstrumentFeatures(instrumentIds, writeFeatures=True)
        print(self.__trainingFeatureManager.getInstrumentDf('IBM', chunkSize=100))

    def getFeatureSet(self):
        pass

    def computeFeatures(self):
        pass

    def findBestModel(self):
        pass

    def getFinalMetrics(self):
        pass

if __name__ == '__main__':
    cachedFolderName='yahooData/'
    dataSetId='testTrading'
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2013/05/10'
    endDateStr = '2017/10/09'
    mlsParams = ModelLearningSystemParamters(instrumentIds, 'XYZ', chunkSize=1000)
    params = dict(cachedFolderName='yahooData/',
                 dataSetId='testTrading',
                 instrumentIds=instrumentIds,
                 startDateStr=startDateStr,
                 endDateStr=endDateStr,
                 event='history',
                 liveUpdates=False)
    mlsParams.initializeDataSource('abc', **params)

    # mlsParams.trainingDataSource = YahooStockDataSource()
    # print(mlsParams.trainingDataSource.emitAllInstrumentUpdates()['IBM'].getBookData())

    system1 = ModelLearningSystem(mlsParams)
    print(system1.getTrainingInstrurmentData('IBM').getBookData())
