from backtester.features.feature_config import FeatureConfig
from backtester.featureSelection.feature_selection_config import FeatureSelectionConfig
from backtester.transformers.transformer_config import FeatureTransformationConfig
from backtester.predefinedModels.model_config import ModelConfig
from backtester.features.feature import Feature
from backtester.mlMetrics.metric_config import MetricConfig
from backtester.constants import *
from backtester.logger import *
from datetime import timedelta
from datetime import datetime
from dateutil import parser
from fractions import Fraction
import numpy as np
import pandas as pd

class ModelLearningSystemParamters(object):
    def __init__(self, symbols, chunkSize=None, modelDir='savedModels'):
        self.instrumentIds = symbols
        self.chunkSize = chunkSize
        self.modelDir = modelDir
        self.dataSourceTypes = ['training', 'validation', 'test']
        self.startDateStr = {}
        self.endDateStr = {}
        self.dropFeatures = self.getFeaturesToDrop()

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
    def getDataSourceName(self):
        return 'YahooStockDataSource'

    def getDataSourceBaseParams(self):
        return dict( cachedFolderName='yahooData/',
                     dataSetId='testTrading',
                     instrumentIds=self.instrumentIds)

    def getDataSourceParams(self, dataSourceType, dataSourceName, dataSourceBaseParams):
        if self.startDateStr[dataSourceType] is None or self.endDateStr[dataSourceType] is None:
            return None
        params = dataSourceBaseParams.copy()
        params['dataSourceName'] = dataSourceName
        params['featureFolderName'] = '%sFeatures' % dataSourceType
        params['dropFeatures'] = self.dropFeatures
        params['startDateStr'] = self.startDateStr[dataSourceType]
        params['endDateStr'] = self.endDateStr[dataSourceType]
        params['liveUpdates'] = False
        return params

    def getTrainingDataSourceParams(self):
        return self.getDataSourceParams('training', self.getDataSourceName(), self.getDataSourceBaseParams())

    def getValidationDataSourceParams(self):
        return self.getDataSourceParams('validation', self.getDataSourceName(), self.getDataSourceBaseParams())

    def getTestDataSourceParams(self):
        return self.getDataSourceParams('test', self.getDataSourceName(), self.getDataSourceBaseParams())

    def splitData(self, ratio, startDateStr, endDateStr):
        # NOTE: Length of ratio and dataSourceTypes must be same
        # To skip a dataSourceType, set the corresponding ratio value to 0
        if len(ratio) != len(self.dataSourceTypes):
            raise ValueError
        startDate = parser.parse(startDateStr)
        endDate = parser.parse(endDateStr)
        start = startDate
        sumFraction = Fraction(sum(ratio)).limit_denominator()
        for r, key in zip(ratio, self.dataSourceTypes):
            if r == 0:
                self.startDateStr[key] = None
                self.endDateStr[key] = None
                continue
            rFraction = Fraction(r).limit_denominator()
            days = ((endDate - startDate + timedelta(1)) * rFraction.numerator * sumFraction.denominator) / (rFraction.denominator * sumFraction.numerator)
            self.startDateStr[key] = start.strftime('%Y/%m/%d')
            self.endDateStr[key] = (start + days - timedelta(1)).strftime('%Y/%m/%d')
            start = start + days

    def getInstrumentIds(self):
        return self.instrumentIds

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

        explained_variance_score_metric = {'metricKey' : 'explained_variance_score',
                                    'metricId' : 'explained_variance_score',
                                    'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [explained_variance_score_metric]}

    def getMetricSelectionKey(self):
        variance = 'explained_variance_score'
        accuracy = 'accuracy_score_metric'

        return variance

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
    def getFeaturesToDrop(self):
        if len(self.getTargetVariableConfigDicts()) == 0:
            return []
        # These features (or columns), if present in CSV files, will be dropped
        return [tv['featureKey'] for tv in self.getTargetVariableConfigDicts()[INSTRUMENT_TYPE_STOCK]]

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getTargetVariableKeys(self):
        if len(self.getTargetVariableConfigDicts()) == 0:
            return []
        return [tv['featureKey'] for tv in self.getTargetVariableConfigDicts()[INSTRUMENT_TYPE_STOCK]]

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
class MLSTrainingPredictionFeature(Feature):
    SELECTED_FEATURES = {}
    TRANSFORMERS = {}
    MODELS = {}

    @classmethod
    def transformData(cls, instrumentId, X):
        transformers = cls.TRANSFORMERS.get(instrumentId, None)
        if transformers is None:
            return X
        transformers = transformers.values() if isinstance(transformers, dict) else transformers
        for transformer in transformers:
            X = transformer.transform(X)
        return X

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        predictions = pd.Series(0.5, index=instrumentManager.getAllInstrumentsByInstrumentId())
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        for instrumentId in instrumentManager.getAllInstrumentsByInstrumentId():
            X = []
            for feature in cls.SELECTED_FEATURES[instrumentId]:
                X.append(lookbackInstrumentFeatures.getFeatureDf(feature)[instrumentId].iloc[-1])
            X = np.array(X).reshape(1, -1)
            X = cls.transformData(instrumentId, X)
            predictions[instrumentId] = cls.MODELS[instrumentId].predict(X)
        return predictions
