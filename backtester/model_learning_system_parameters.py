from backtester.features.feature_config import FeatureConfig
from backtester.featureSelection.feature_selection_config import FeatureSelectionConfig
from backtester.transformers.transformer_config import FeatureTransformationConfig
from backtester.predefinedModels.model_config import ModelConfig
from backtester.constants import *
from backtester.logger import *


class ModelLearningSystemParamters(object):
    def __init__(self, symbols, chunkSize=None, validationSplit=0.1):
        self.instrumentIds = symbols
        self.chunkSize = chunkSize
        self.validationSplit = validationSplit

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

    def getTrainingDataSourceParams(self):
        startDateStr = '2010/06/02'
        endDateStr = '2012/02/07'
        return dict( dataSourceName='CsvDataSource',
                     featureFolderName='trainingFeatures',
                     dropFeatures=['Y'],
                     ## Now Datasource parameters ##
                     cachedFolderName='historicalData/',
                     dataSetId='QQ3Data',
                     instrumentIds=self.instrumentIds,
                     downloadUrl='https://raw.githubusercontent.com/Auquan/qq3Data/master',
                     timeKey='datetime',
                     timeStringFormat='%Y-%m-%d %H:%M:%S',
                     startDateStr=startDateStr,
                     endDateStr=endDateStr,
                     liveUpdates=False)

    def getValidationDataSourceParams(self):
        raise NotImplementedError

    def getTestDataSourceParams(self):
        startDateStr = '2012/02/08'
        endDateStr = '2013/02/07'
        return dict( dataSourceName='CsvDataSource',
                     featureFolderName='testFeatures',
                     dropFeatures=['Y'],
                     ## Now Datasource parameters ##
                     cachedFolderName='historicalData/',
                     dataSetId='QQ3Data',
                     instrumentIds=self.instrumentIds,
                     downloadUrl='https://raw.githubusercontent.com/Auquan/qq3Data/master',
                     timeKey='datetime',
                     timeStringFormat='%Y-%m-%d %H:%M:%S',
                     startDateStr=startDateStr,
                     endDateStr=endDateStr,
                     liveUpdates=False)

    def getInstrumentIds(self):
        return self.instrumentIds

    def getInstrumentFeatureConfigDicts(self):
        # ma2Dict = {'featureKey': 'ma_5',
        #            'featureId': 'moving_average',
        #            'params': {'period': 5,
        #                       'featureName': 'Open'}}

        return {INSTRUMENT_TYPE_STOCK : []}

    def getTargetVariableConfigDicts(self):
        # tv_ma25 = {'featureKey' : 'tv_ma25',
        #            'featureId' : 'moving_average',
        #            'params' : {'period' : 25,
        #                        'featureName' : 'ma_5',
        #                        'shift' : 10}}
        # tv_ma5 = {'featureKey' : 'tv_ma5',
        #            'featureId' : 'moving_average',
        #            'params' : {'period' : 5,
        #                        'featureName' : 'ma_5',
        #                        'shift' : 5}}
        Y = {'featureKey' : 'Y',
             'featureId' : '',
             'params' : {}}

        return {INSTRUMENT_TYPE_STOCK : [Y]}

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
                         'params' : {'scoreFunction' : 'f_classif',
                                     'mode' : 'k_best',
                                     'modeParam' : 30}}
        return {INSTRUMENT_TYPE_STOCK : [genericSelect]}

    def getFeatureTransformationConfigDicts(self):
        stdScaler = {'featureTransformKey': 'stdScaler',
                     'featureTransformId' : 'standard_transform',
                     'params' : {}}

        minmaxScaler = {'featureTransformKey' : 'minmaxScaler',
                        'featureTransformId' : 'minmax_transform',
                        'params' : {'low' : -1,
                                    'high' : 1}}
        return {INSTRUMENT_TYPE_STOCK : [stdScaler]}

    def getModelConfigDicts(self):
        regression_model = {'modelKey': 'linear_regression',
                     'modelId' : 'linear_regression',
                     'params' : {}}

        classification_model = {'modelKey': 'logistic_regression',
                     'modelId' : 'logistic_regression',
                     'params' : {}}
        return {INSTRUMENT_TYPE_STOCK : [classification_model]}

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
