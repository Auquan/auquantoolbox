import sys, os
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from backtester.model_learning_system_parameters import ModelLearningSystemParamters
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.feature_manager import FeatureManager


class ModelLearningSystem:
    def __init__(self, mlsParams, chunkSize=None):
        self.mlsParams = mlsParams
        self.__targetVariable = self.mlsParams.getTargetVariable()
        self.__trainingDataSource = self.mlsParams.getTrainingDataSource()
        self.__validationDataSource = self.mlsParams.getValidationDataSource()
        self.__testDataSource = self.mlsParams.getTestDataSource()
        self.__trainingFeatureManager = FeatureManager(self.mlsParams, self.__trainingDataSource, chunkSize)

    def generateFeatures(self):
        self.__trainingFeatureManager.computeInstrumentFeatures(writeFeatures=True)
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
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2013/05/10'
    endDateStr = '2017/06/09'
    mlsParams = ModelLearningSystemParamters(instrumentIds, 'XYZ')
    mlsParams.trainingDataSource = YahooStockDataSource(cachedFolderName='yahooData/',
                                     dataSetId="testTrading",
                                     instrumentIds=instrumentIds,
                                     startDateStr=startDateStr,
                                     endDateStr=endDateStr,
                                     event='history',
                                     liveUpdates=False)

    system1 = ModelLearningSystem(mlsParams, chunkSize=1000)
    system1.generateFeatures()
