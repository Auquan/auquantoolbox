from backtester.features.feature_config import FeatureConfig
from backtester.featureSelection.feature_selection_config import FeatureSelectionConfig
from backtester.transformers.transformer_config import FeatureTransformationConfig
from backtester.predefinedModels.model_config import ModelConfig
from backtester.constants import *
from backtester.logger import *
from dateutil import parser
from datetime import timedelta
from datetime import datetime
from dateutil import parser

class ModelLearningSystemParamters(object):
    def __init__(self, symbols, chunkSize=None, validationSplit=0.1):
        self.instrumentIds = symbols
        self.chunkSize = chunkSize
        self.validationSplit = validationSplit
        self.startDateStr = {'training':'2013/02/02' , 'test':'2015/02/03'}
        self.endDateStr = {'training': '2015/02/02', 'test':'2017/02/02'}

        FeatureConfig.setupCustomFeatures(self.getCustomFeatures())
        FeatureSelectionConfig.setupCustomFeatureSelectionMethods(self.getCustomFeatureSelectionMethods())
        FeatureTransformationConfig.setupCustomFeatureTransformationMethods(self.getCustomFeatureTransformationMethods())
        ModelConfig.setupCustomModelMethods(self.getCustomModelMethods())

        self.__instrumentFeatureConfigs = {}
        instrumentFeatureConfigDicts = self.getInstrumentFeatureConfigDicts()
        for instrumentType in instrumentFeatureConfigDicts:
            if type(instrumentFeatureConfigDicts[instrumentType]) is list:
                self.__instrumentFeatureConfigs[instrumentType] = list(map(lambda x: FeatureConfig(x), instrumentFeatureConfigDicts[instrumentType]))
            elif type(instrumentFeatureConfigDicts[instrumentType]) is dict:
                self.__instrumentFeatureConfigs[instrumentType] = {k : FeatureConfig(v) for k, v in instrumentFeatureConfigDicts[instrumentType]}
            else:
                logError("Unknown type of instruments' feature config dicts")

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

        self.dropFeatures = self.getFeaturesToDrop()

    def getInstrumentIds(self):
        return self.instrumentIds

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

    def getDataSourceName(self):
        return 'YahooStockDataSource'

    def getDataSourceBaseParams(self):
        return dict( cachedFolderName='yahooData/',
                     dataSetId='testTrading',
                     instrumentIds=self.instrumentIds)


    def getTrainingDataSourceParams(self):
        # raise NotImplementedError
        return self.getDataSourceParams('training', self.getDataSourceName(), self.getDataSourceBaseParams())

    def getValidationDataSourceParams(self):
        raise NotImplementedError

    def getTestDataSourceParams(self):
        # raise NotImplementedError
        return self.getDataSourceParams('test', self.getDataSourceName(), self.getDataSourceBaseParams())


    def splitData(self, ratio, startDate, endDate, dataSourceTypes):
        # NOTE: Length of ratio and dataSourceTypes must be same
        # To skip a dataSourceType, set the corresponding ratio value to 0
        if len(ratio) != len(dataSourceTypes):
            raise ValueError
        startDate = parser.parse(startDate)
        endDate = parser.parse(endDate)
        start = startDate
        for r, key in zip(ratio, dataSourceTypes):
            if r == 0:
                self.startDateStr[key] = None
                self.endDateStr[key] = None
                continue
            days = ((endDate - startDate + timedelta(1)).days * r) / sum(ratio)
            self.startDateStr[key] = start.strftime('%Y/%m/%d')
            self.endDateStr[key] = (start + timedelta(days=days) - timedelta(1)).strftime('%Y/%m/%d')
            start = start + timedelta(days=days)

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
        tv_ma25 = {'featureKey' : 'tv_ma25',
                   'featureId' : 'moving_average',
                   'params' : {'period' : 25,
                               'featureName' : 'ma_5',
                               'shift' : 10}}
        tv_ma5 = {'featureKey' : 'tv_ma5',
                   'featureId' : 'moving_average',
                   'params' : {'period' : 5,
                               'featureName' : 'ma_5',
                               'shift' : 5}}
        Y = {'featureKey' : 'Y',
             'featureId' : '',
             'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [tv_ma25, tv_ma5]}

    def getFeaturesToDrop(self):
        # These features (or columns), if present in CSV files, will be dropped
        return [tv['featureKey'] for tv in self.getTargetVariableConfigDicts()[INSTRUMENT_TYPE_STOCK]]

    def getFeatureSelectionConfigDicts(self):
        corr = {'featureSelectionKey': 'corr',
                'featureSelectionId' : 'pearson_correlation',
                'params' : {'startPeriod' : 0,
                            'endPeriod' : 60,
                            'steps' : 10,
                            'threshold' : 0.1,
                            'topK' : 2}}

        genericSelect = {'featureSelectionKey' : 'gus',
                         'featureSelectionId' : 'generic_univariate_select',
                         'params' : {'scoreFunction' : 'f_regression',
                                     'mode' : 'k_best',
                                     'modeParam' : 12}}

        rfecvSelect = {'featureSelectionKey': 'rfecv',
                       'featureSelectionId': 'rfecv_selection',
                       'params' : {'estimator' : 'LinearRegression',
                       'estimator_params' : {},
                       'step' : 1,
                       'cv' : None,
                       'scoring' : None,
                       'n_jobs' : 2}}

        return {INSTRUMENT_TYPE_STOCK : [genericSelect]}

    def getFeatureTransformationConfigDicts(self):
        stdScaler = {'featureTransformKey': 'stdScaler',
                     'featureTransformId' : 'standard_transform',
                     'params' : {}}

        minmaxScaler = {'featureTransformKey' : 'minmaxScaler',
                        'featureTransformId' : 'minmax_transform',
                        'params' : {'low' : -1,
                                    'high' : 1}}

        pcaScaler = {'featureTransformKey' : 'pcaScaler',
                     'featureTransformId' : 'pca_transform',
                     'params' : {'n_comp' : 6,
                                 'copy' : True,
                                 'whiten' : False,
                                 'svd' : 'full',
                                 'itr_power' : 'auto',
                                 'random_state' : None}}

        return {INSTRUMENT_TYPE_STOCK : [pcaScaler, minmaxScaler]}

    def getModelConfigDicts(self):
        regression_model = {'modelKey': 'linear_regression',
                     'modelId' : 'linear_regression',
                     'params' : {}}

        classification_model = {'modelKey': 'logistic_regression',
                     'modelId' : 'logistic_regression',
                     'params' : {}}
        return {INSTRUMENT_TYPE_STOCK : [regression_model]}

    def getCustomFeatures(self):
        return {}

    def getCustomFeatureSelectionMethods(self):
        return {}

    def getCustomFeatureTransformationMethods(self):
        return {}

    def getCustomModelMethods(self):
        return {}

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

    def getTrainingDataSource(self):
        return self.trainingDataSource

    def getValidationDataSource(self):
        return self.validationDataSource

    def getTestDataSource(self):
        return self.testDataSource
