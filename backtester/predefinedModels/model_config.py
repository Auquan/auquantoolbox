from backtester.configurator import Configurator
from backtester.predefinedModels.model_template import Model
from backtester.predefinedModels.regressionModels.linear_regression import LinearRegression
from backtester.predefinedModels.classificationModels.logistic_regression import LogisticRegression
from backtester.predefinedModels.classificationModels.support_vector_machine import SupportVectorMachine
from backtester.predefinedModels.classificationModels.mlp_classification import MultiLayerPerceptronClassification
from backtester.predefinedModels.regressionModels.mlp_regression import MultiLayerPerceptronRegression
from backtester.logger import *

modelIdToClassDict = {'linear_regression' : LinearRegression,
                      'logistic_regression' : LogisticRegression,
                      'support_vector_machine': SupportVectorMachine,
                      'mlp_classification' : MultiLayerPerceptronClassification,
                      'mlp_regression' : MultiLayerPerceptronRegression}

class ModelConfig(Configurator):
    """
    Configures feature selection dicts
    """

    customIdToClassDict = {}

    def __init__(self, configDict):
        super(ModelConfig, self).__init__()

        if 'modelId' not in configDict:
            logError('modelId missing in config dictionary %s', configDict['modelKey'])
            # TODO:  Raise appropriate error
        self._identifier = configDict['modelId']

        self._key = configDict.get('modelKey', self._identifier)
        self._params = configDict.get('params', {})

    @classmethod
    def setupCustomModelMethods(cls, customIdToClass):
        ModelConfig.customIdToClassDict.update(customIdToClass)

    @classmethod
    def getClassForModelId(cls, modelId):
        if modelId in ModelConfig.customIdToClassDict:
            return ModelConfig.customIdToClassDict[modelId]
        return cls.getClassForId(modelId, modelIdToClassDict, Model)
