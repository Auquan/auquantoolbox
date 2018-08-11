import pandas as pd
import copy
try:        # Python 3.x
    import _pickle as pickle
except ImportError:
    try:    # Python 2.x
        import cPickle as pickle
    except ImportError:
        import pickle
from backtester.constants import *
from backtester.logger import *

class TrainingModelManager(object):
    """
    Base training model manager class to read, write, fit, predict and re-train
    """
    # TODO: process multiple model fit parallely

    def __init__(self, systemParams):
        self.systemParams = systemParams
        self._trainingModel = {}
        self._modelKeyPool = 1      # NOTE: Vulnerable to overflow :P

    def setTargetVariable(self, targetVariable):
        self._targetVariable = targetVariable

    def getModel(self):
        return copy.deepcopy(self._trainingModel)

    # add or update the model in the _trainingModel dict
    def addModel(self, model, modelKey=None):
        if modelKey is None:
            modelKey = str(self._modelKeyPool)
            self._modelKeyPool += 1
        self._trainingModel.update({modelKey : model})
        return modelKey

    # add or update the models in the _trainingModel dict
    def addModels(self, models):
        for modelKey in models:
            self.addModel(models[modelKey], modelKey)

    def getModelByConfig(self, modelConfig):
        return self._trainingModel[modelConfig.getKey()]

    def readModel(self, fileName):
        with open(fileName, 'rb') as f:
            self._trainingModel = pickle.load(f)

    def writeModel(self, fileName):
        with open(fileName, 'wb') as f:
            pickle.dump(self._trainingModel, f)

    def computeWorkingTimestamps(self, data):
        timestamps = None
        if isinstance(data, dict):
            for key in data:
                if timestamps is None:
                    timestamps = data[key].index
                else:
                    timestamps = data[key].index.intersection(timestamps)
        elif isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            timestamps = data.index
        else:
            return None
        return timestamps

    def modelConfigWrapper(func):
        def wrapper(self, *args, **kwargs):
            modelConfigs = kwargs.get('modelConfigs', None)
            modelConfigs = kwargs.get('modelConfig', None) if modelConfigs is None else modelConfigs
            outputDict = {}
            if modelConfigs is None:
                modelConfigs = self.systemParams.getModelConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
            elif not isinstance(modelConfigs, list):
                modelConfigs = [modelConfigs]
            for modelConfig in modelConfigs:
                outputDict[modelConfig.getKey()] = func(self, *args, modelConfig=modelConfig)
            return outputDict
        return wrapper

    # fit multiple models on the same dataset
    @modelConfigWrapper
    def fitModel(self, features, targetVariable, modelConfig):
        timestamps = self.computeWorkingTimestamps(targetVariable)
        if timestamps is not None and (isinstance(features, pd.DataFrame) or isinstance(features, pd.Series)):
            features = features.loc[timestamps]
        modelKey = modelConfig.getKey()
        modelId = modelConfig.getId()
        modelParams = modelConfig.getParams()
        modelCls = modelConfig.getClassForModelId(modelId)
        self._trainingModel[modelKey] = modelCls(modelParams)
        return self._trainingModel[modelKey].fit(features, targetVariable)

    @modelConfigWrapper
    def predict(self, features, modelConfig):
        return self._trainingModel[modelConfig.getKey()].predict(features)

    @modelConfigWrapper
    def reTrain(self, features, targetVariable, modelConfig):
        timestamps = self.computeWorkingTimestamps(targetVariable)
        if timestamps is not None and (isinstance(features, pd.DataFrame) or isinstance(features, pd.Series)):
            features = features.loc[timestamps]
        return self._trainingModel[modelConfig.getKey()].reTrain(features, targetVariable)

    @modelConfigWrapper
    def evaluateModel(self, features, targetVariable, modelConfig):
        timestamps = self.computeWorkingTimestamps(targetVariable)
        if timestamps is not None and (isinstance(features, pd.DataFrame) or isinstance(features, pd.Series)):
            features = features.loc[timestamps]
        return self._trainingModel[modelConfig.getKey()].evaluate(features, targetVariable)

    def dumpModel(self, modelConfig):
        modelKey = modelConfig.getKey()
        del self._trainingModel[modelKey]

    def flushTrainingModels(self):
        keys = list(self._trainingModel.keys())
        for key in keys:
            del self._trainingModel[key]
        del self._trainingModel
        self._trainingModel = {}
