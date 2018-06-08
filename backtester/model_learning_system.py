import sys


class ModelLearningSystem:
    def __init__(self,mlsParams):
        self.mlsParams = mlsParams
        self.__targetVariable = self.mlsParams.getTargetVariable()
        self.__trainingDataSource = self.mlsParams.getTrainingDataSource()
        self.__validationDataSource = self.mlsParams.getValidationDataSource()
        self.__testDataSource = self.mlsParams.getTestDataSource()
        self.__trainingFeatureManager = FeatureManager(self.mlsParams, self.__trainingDataSource)


    def getFeatureSet(self):
        pass

    def computeFeatures(self):
        pass

    def findBestModel(self):
        pass

    def getFinalMetrics(self):
        pass
