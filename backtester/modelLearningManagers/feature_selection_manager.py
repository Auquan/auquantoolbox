import pandas as pd
from backtester.constants import *
from backtester.logger import *

class FeatureSelectionManager(object):
    """
    Selects features which are important for a target variable from the pool of feature set
    """

    # TODO:  Implement the support for selecting features when instrument data is in chunks

    def __init__(self, systemParams):
        self.systemParams = systemParams
        self.__instrumentData = None
        self.__targetVariables = None
        self.__currentTimestamps = None
        self.__selectedFeatures = {}

    def getFeatureDf(self, featureKey):
        return self.__instrumentData[featureKey].loc[self.__currentTimestamps]

    def getTargetVariableDf(self, targetVariableKey):
        return self.__targetVariables[targetVariableKey]

    def getAllSelectedFeaturesByKey(self, targetVariableKey):
        return self.__selectedFeatures[targetVariableKey]

    def getAllSelectedFeatures(self):
        return self.__selectedFeatures

    def getKeysFromData(self, data):
        if isinstance(data, dict):
            return data.keys()
        elif isinstance(data, pd.DataFrame):
            return data.columns.tolist()
        else:
            raise ValueError

    def pruneFeatures(self, instrumentData, targetVariables, featureSelectionConfigs=None, aggregationMethod='intersect'):
        if featureSelectionConfigs is None:
            featureSelectionConfigs = self.systemParams.getFeatureSelectionConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        featureKeys = self.getKeysFromData(instrumentData)
        targetVariableKeys = self.getKeysFromData(targetVariables)

        if len(featureSelectionConfigs) == 0:
            self.__selectedFeatures = {key : instrumentData.columns.tolist() for key in targetVariableKeys}
            return

        self.__instrumentData = instrumentData
        self.__targetVariables = targetVariables
        self.__selectedFeatures = {key : [] for key in targetVariableKeys}

        for targetVariableKey in targetVariableKeys:
            self.__currentTimestamps = self.__targetVariables[targetVariableKey].index
            for featureSelectionConfig in featureSelectionConfigs:
                featureSelectionKey = featureSelectionConfig.getKey()
                featureSelectionParams = featureSelectionConfig.getParams()
                featureSelectionId = featureSelectionConfig.getId()
                featureSelectionCls = featureSelectionConfig.getClassForFeatureSelectonId(featureSelectionId)
                selectedFeatures = featureSelectionCls.extractImportantFeatures(targetVariableKey, featureKeys,
                                                                                  featureSelectionParams, self)
                if self.__selectedFeatures[targetVariableKey] == []:
                    self.__selectedFeatures[targetVariableKey] = selectedFeatures
                elif aggregationMethod == 'union':
                    self.__selectedFeatures[targetVariableKey] = list(set(selectedFeatures).union(self.__selectedFeatures[targetVariableKey]))
                elif aggregationMethod == 'intersect':
                    self.__selectedFeatures[targetVariableKey] = list(set(selectedFeatures).intersection(self.__selectedFeatures[targetVariableKey]))
                else:
                    raise ValueError

    def flushSelectedFeatures(self):
        keys = list(self.__selectedFeatures.keys())
        for key in keys:
            del self.__selectedFeatures[key]
        del self.__selectedFeatures
        self.__selectedFeatures = {}
