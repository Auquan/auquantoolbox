from backtester.features.feature_config import FeatureConfig
import sys


class ModelLearningSystemParamters(Object):
    def __init__(self, symbols, targetVariable, models=None):
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
