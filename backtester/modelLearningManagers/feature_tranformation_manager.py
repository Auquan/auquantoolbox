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

class FeatureTransformationManager(object):
    """
    """
    def __init__(self, systemParams, transformerFileName=''):
        self.systemParams = systemParams
        self.__fileName = transformerFileName
        self.__instrumentData = None
        self.__transformedData = None
        self.__transformers = {}

    def getInstrumentData(self):
        return self.__instrumentData

    def getTransformedData(self):
        return self.__instrumentData

    def readTransformers(self):
        with open(self.__fileName, 'rb') as f:
            self.__transformers = pickle.load(f)

    def writeTransformers(self, fileName):
        with open(fileName, 'wb') as f:
            pickle.dump(self.__transformers, f)

    def transformFeaturesUsingFile(self, instrumentData, transformationConfigs=None):
        self.__instrumentData = instrumentData
        if transformationConfigs is None:
            transformerKeys = self.__transformers.keys()
        else:
            transformerKeys = [config.getFeatureKey() for config in transformationConfigs]
        for key in transformerKeys:
            self.__instrumentData = self.__transformers[key].transform(self)

    def transformFeatures(self, instrumentData, transformationConfigs=None):
        if transformationConfigs is None:
            transformationConfigs = self.systemParams.getFeatureTransformationConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        self.__instrumentData = instrumentData
        for transformationConfig in transformationConfigs:
            transformationKey = transformationConfig.getFeatureKey()
            transformationId = transformationConfig.getFeatureId()
            transformationParams = transformationConfig.getFeatureParams()
            transformationCls = transformationConfig.getClassForFeatureId(transformationId)
            self.__transformers[transformationKey] = transformationCls(transformationParams)
            self.__instrumentData = self.__transformers[transformationKey].transform(self)
