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
    performs series of transformation on the instrument data
    """

    # TODO: Implement the support for transforming features in chunks

    def __init__(self, systemParams, transformerFileName=''):
        self.systemParams = systemParams
        self.__instrumentData = None
        self.__transformers = {}
        if transformerFileName == '':
            self.transformFeatures = self._transformFeaturesUsingConfigs
        else:
            self.readTransformers(transformerFileName)

    def getInstrumentData(self):
        return self.__instrumentData

    def getTransformedData(self):
        return self.__instrumentData

    def readTransformers(self, fileName):
        with open(fileName, 'rb') as f:
            self.__transformers = pickle.load(f)
        self.transformFeatures = self._transformFeaturesUsingFile

    def writeTransformers(self, fileName):
        with open(fileName, 'wb') as f:
            pickle.dump(self.__transformers, f)

    def setTransformers(self, transformers):
        self.__transformers = transformers
        self.transformFeatures = self._transformFeaturesUsingFile

    def _transformFeaturesUsingFile(self, instrumentData, transformationConfigs=None):
        self.__instrumentData = instrumentData
        if transformationConfigs is None:
            transformerKeys = self.__transformers.keys()
        else:
            transformerKeys = [config.getKey() for config in transformationConfigs]
        for key in transformerKeys:
            self.__instrumentData = self.__transformers[key].transform(self)

    def _transformFeaturesUsingConfigs(self, instrumentData, transformationConfigs=None):
        if transformationConfigs is None:
            transformationConfigs = self.systemParams.getFeatureTransformationConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        self.__instrumentData = instrumentData
        for transformationConfig in transformationConfigs:
            transformationKey = transformationConfig.getKey()
            transformationId = transformationConfig.getId()
            transformationParams = transformationConfig.getParams()
            transformationCls = transformationConfig.getClassForFeatureTransformationId(transformationId)
            self.__transformers[transformationKey] = transformationCls(transformationParams)
            self.__instrumentData = self.__transformers[transformationKey].transform(self)
