from market_feature import MarketFeature
from backtester.logger import *
from ratio_feature import RatioFeature
from moving_average_feature import MovingAverageInstrumentFeature
from moving_sdev_feature import MovingSdevInstrumentFeature

featureIdToFeatureCls = {'ratio': RatioFeature,
                         'moving_average' : MovingAverageInstrumentFeature,
                         'moving_sdev' : MovingSdevInstrumentFeature }


class MarketFeatureConfig:

    customFeatureIdToFeatureCls = {}

    def __init__(self, configDict):
        if 'featureId' not in configDict:
            logError('featureId missing in market feature config dictionary')
        self.__featureIdentifier = configDict['featureId']

        if 'featureKey' in configDict:
            self.__featureKey = configDict['featureKey']
        else:
            self.__featureKey = self.__featureIdentifier

        if 'params' in configDict:
            self.__featureParams = configDict['params']
        else:
            self.__featureParams = {}

    def getFeatureKey(self):
        return self.__featureKey

    def getFeatureId(self):
        return self.__featureIdentifier

    def getFeatureParams(self):
        return self.__featureParams

    @classmethod
    def setupCustomMarketFeatures(cls, customFeatureIdToFeatureCls):
        MarketFeatureConfig.customFeatureIdToFeatureCls = customFeatureIdToFeatureCls

    @classmethod
    def getClassForMarketFeatureId(cls, marketFeatureId):
        if marketFeatureId in MarketFeatureConfig.customFeatureIdToFeatureCls:
            return MarketFeatureConfig.customFeatureIdToFeatureCls[marketFeatureId]
        if marketFeatureId in featureIdToFeatureCls:
            return featureIdToFeatureCls[marketFeatureId]
        logError('%s not a valid market feature Id. Use a predefined one or provide a custom implementation' % marketFeatureId)
        return MarketFeature
