import pandas as pd
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
    """
    def __init__(self, systemParams):
        self.systemParams = systemParams
        self._features = None
        self._targetVariable = None
        self._trainingModel = None

    def getFeaures(self):
        return self._features

    def getTargetVariable(self):
        return self._targetVariable

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
        elif isinstance(data, pd.DataFrame) or isinstance(data, pd.Seires):
            timestamps = data.index
        else:
            raise ValueError
        return timestamps

    def fitModel(self, features, targetVariable, modelConfigs=None):
        self._targetVariable = targetVariable
        self._features = features.loc[self.computeWorkingTimestamps(targetVariable)]

        if modelConfigs is None:
            modelConfigs = self.systemParams.getModelConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        for modelConfig in modelConfigs:
            modelKey = modelConfig.getKey()
            modelId = modelConfig.getId()
            modelParams = modelConfig.getParams()
            modelCls = modelConfig.getClassForModelId(modelId)
            self._trainingModel[modelKey] = modelCls(modelParams)
            self._trainingModel[modelKey].fit(self)
