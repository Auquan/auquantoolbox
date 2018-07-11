import sys, os
from backtester.features.feature_config import FeatureConfig
from backtester.featureSelection.feature_selection_config import FeatureSelectionConfig
from backtester.transformers.transformer_config import FeatureTransformationConfig
from backtester.predefinedModels.model_config import ModelConfig
from backtester.mlMetrics.metric_config import MetricConfig
from backtester.constants import *
from backtester.logger import *


class ModelLearningSystemParamters(object):
    def __init__(self, symbols, chunkSize=None, modelDir='savedModels'):
        self.instrumentIds = symbols
        self.chunkSize = chunkSize
        self.modelDir = modelDir

        FeatureConfig.setupCustomFeatures(self.getCustomFeatures())
        FeatureSelectionConfig.setupCustomFeatureSelectionMethods(self.getCustomFeatureSelectionMethods())
        FeatureTransformationConfig.setupCustomFeatureTransformationMethods(self.getCustomFeatureTransformationMethods())
        ModelConfig.setupCustomModelMethods(self.getCustomModelMethods())
        MetricConfig.setupCustomMetricMethods(self.getCustomMetricMethods())

        self.__instrumentFeatureConfigs = {}
        instrumentFeatureConfigDicts = self.getInstrumentFeatureConfigDicts()
        for instrumentType in instrumentFeatureConfigDicts:
                self.__instrumentFeatureConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), instrumentFeatureConfigDicts[instrumentType]))

        self.__targetVariableConfigs = {}
        targetVariableConfigDicts = self.getTargetVariableConfigDicts()
        for instrumentType in targetVariableConfigDicts:
            self.__targetVariableConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), targetVariableConfigDicts[instrumentType]))

        self.__featureSelectionConfigs = {}
        featureSelectionConfigDicts = self.getFeatureSelectionConfigDicts()
        for instrumentType in featureSelectionConfigDicts:
            self.__featureSelectionConfigs[instrumentType] = list(map(lambda x: FeatureSelectionConfig(x), featureSelectionConfigDicts[instrumentType]))

        self.__featureTransformationConfigs = {}
        featureTransformationConfigDicts = self.getFeatureTransformationConfigDicts()
        for instrumentType in featureTransformationConfigDicts:
            self.__featureTransformationConfigs[instrumentType] = list(map(lambda x: FeatureTransformationConfig(x), featureTransformationConfigDicts[instrumentType]))

        self.__modelConfigs = {}
        ModelConfigDicts = self.getModelConfigDicts()
        for instrumentType in ModelConfigDicts:
            self.__modelConfigs[instrumentType] = list(map(lambda x: ModelConfig(x), ModelConfigDicts[instrumentType]))

        self.__metricConfigs = {}
        MetricConfigDicts = self.getMetricConfigDicts()
        for instrumentType in MetricConfigDicts:
            self.__metricConfigs[instrumentType] = list(map(lambda x: MetricConfig(x), MetricConfigDicts[instrumentType]))

    def getInstrumentIds(self):
        return self.instrumentIds

    def getTrainingDataSourceParams(self):
        raise NotImplementedError

    def getValidationDataSourceParams(self):
        return None

    def getTestDataSourceParams(self):
        raise NotImplementedError

    def getInstrumentFeatureConfigDicts(self):
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'Open'}}

        argMax = {'featureKey': 'argmax',
                   'featureId': 'argmax',
                   'params': {'period': 5,
                              'featureName': 'Open'}}

        argMin = {'featureKey': 'argmin',
                   'featureId': 'argmin',
                   'params': {'period': 5,
                              'featureName': 'Open'}}

        bollinger_Lower = {'featureKey': 'bblf',
                     'featureId': 'bollinger_bands_lower',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        bollinger_Upper = {'featureKey': 'bblu',
                     'featureId': 'bollinger_bands_upper',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        delay = {'featureKey': 'delay',
                     'featureId': 'delay',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        difference = {'featureKey': 'diff',
                     'featureId': 'difference',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        direction = {'featureKey': 'dirctn',
                     'featureId': 'direction',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        ema = {'featureKey': 'ema',
                     'featureId': 'exponential_moving_average',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        macd = {'featureKey': 'macd',
                     'featureId': 'macd',
                     'params': {'period1': 5,
                                'period2': 3,
                                'featureName': 'Open'}}

        momentum = {'featureKey': 'momentum',
                     'featureId': 'momentum',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        mov_avg = {'featureKey': 'mov_avg',
                     'featureId': 'moving_average',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        mov_corr = {'featureKey': 'mov_corr',
                     'featureId': 'moving_correlation',
                     'params': {'period': 5,
                                'featureName1': 'Open',
                                'featureName2': 'High'}}

        mmax = {'featureKey': 'mmax',
                     'featureId': 'moving_max',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        mmin = {'featureKey': 'mmin',
                     'featureId': 'moving_min',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        msdev = {'featureKey': 'msdev',
                     'featureId': 'moving_sdev',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        msum = {'featureKey': 'msum',
                     'featureId': 'moving_sum',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        rank = {'featureKey': 'rank',
                     'featureId': 'rank',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        ratio = {'featureKey': 'ratio',
                     'featureId': 'ratio',
                     'params': {'featureName1': 'High',
                                'featureName2': 'Open'}}

        rsi = {'featureKey': 'rsi',
                     'featureId': 'rsi',
                     'params': {'period': 5,
                                'featureName': 'Open'}}

        scale = {'featureKey': 'scale',
                     'featureId': 'scale',
                     'params': {'period': 5,
                                'featureName': 'Open',
                                'scale': 2}}

        vwap = {'featureKey': 'vwap',
                     'featureId': 'vwap',
                     'params': {'askVolume': 'Open',
                                'bidVolume': 'High',
                                'askPrice': 'Low',
                                'bidPrice': 'Close'}}

        return {INSTRUMENT_TYPE_STOCK : [ma2Dict, argMax, argMin, bollinger_Lower, bollinger_Upper, delay,
                                         difference, direction, ema, macd, momentum, mov_avg, mov_corr, mmax, mmin, msdev,
                                         msum, rank, ratio, rsi, scale, vwap]}

    def getTargetVariableConfigDicts(self):
        return {}

    def getFeatureSelectionConfigDicts(self):
        return {}

    def getFeatureTransformationConfigDicts(self):
        return {}

    def getModelConfigDicts(self):
        return {}

    def getMetricConfigDicts(self):
        accuracy_score_metric = {'metricKey' : 'accuracy_score',
                                 'metricId' : 'accuracy_score',
                                 'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [accuracy_score_metric]}

    def getCustomFeatures(self):
        return {}

    def getCustomFeatureSelectionMethods(self):
        return {}

    def getCustomFeatureTransformationMethods(self):
        return {}

    def getCustomModelMethods(self):
        return {}

    def getCustomMetricMethods(self):
        return{}

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__instrumentFeatureConfigs:
            return self.__instrumentFeatureConfigs[instrumentType]
        else:
            return []

    def getTargetVariableConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__targetVariableConfigs:
            return self.__targetVariableConfigs[instrumentType]
        else:
            return []

    def getFeatureSelectionConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__featureSelectionConfigs:
            return self.__featureSelectionConfigs[instrumentType]
        else:
            return []

    def getFeatureTransformationConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__featureTransformationConfigs:
            return self.__featureTransformationConfigs[instrumentType]
        else:
            return []

    def getModelConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__modelConfigs:
            return self.__modelConfigs[instrumentType]
        else:
            return []

    def getMetricConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__metricConfigs:
            return self.__metricConfigs[instrumentType]
        else:
            return []
