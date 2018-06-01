import sys


class ModelLearningSystemParamters:
    """docstring for ModelLearningSystemParamters."""
    def __init__(self, dataSetId):
        self.__dataSetId = dataSetId


    def getInstrumentFeatureConfigDicts(self):
        return {}

    def getDataParser(self):
        raise NotImplementedError
        return None

    def getTrainingData(self):
        pass

    def getValidationData(self):
        pass
