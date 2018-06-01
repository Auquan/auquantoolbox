import sys


class ModelLearningSystem:
    """docstring for ModelLearningSystem."""
    # def __init__(self, mlsParams):
        # self.mlsParams = mlsParams

    def __init__(self, symbols, targetVariable, dataSource, models=None, dateRange=None):
        self.symbols = symbols
        self.targetVariable = targetVariable
        self.dataSource = dataSource


    def getFeatureSet(self):
        pass

    def findBestModel(self):
        pass

    def getFinalMetrics(self):
        pass
