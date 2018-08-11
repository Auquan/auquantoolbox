import copy
try:        # Python 3.x
    import _pickle as pickle
except ImportError:
    try:    # Python 2.x
        import cPickle as pickle
    except ImportError:
        import pickle

class ModelData(object):
    """
    Class to keep all information about a model
    """
    # instrumentIds : string or list of strings
    # targetVariables : targetVariableConfig or list of targetVariableConfig
    # features : list of feature keys (string)
    # transformers : dict
    def __init__(self, instrumentIds, targetVariables, features, transformers, models, modelType=''):
        self.__instrumentIds = instrumentIds if isinstance(instrumentIds, list) else [instrumentIds]
        self.__targetVariables = targetVariables if isinstance(targetVariables, list) else [targetVariables]
        self.__features = features
        self.__transformers = transformers
        self.__models = models
        self.__modelType = modelType
        self.__bestModel = None

    def setBestModel(self, model):
        self.__bestModel = model

    def getInstrumentIds(self):
        return self.__instrumentIds

    def getModelFeatures(self):
        return self.__features

    def getModelTargetVariables(self):
        return self.__targetVariables

    def getModelTransformers(self):
        return self.__transformers

    def getModel(self):
        return self.__bestModel

    def getModels(self):
        return self.__models

    def getModelByModelKey(self, key):
        return self.__models[key]

    def getModelType(self):
        return self.__modelType

    def writeModelData(self, fileName):
        temp = copy.deepcopy(self.__models)
        del self.__models
        with open(fileName, 'wb') as f:
            pickle.dump(self, f)
        self.__models = temp
        return fileName
