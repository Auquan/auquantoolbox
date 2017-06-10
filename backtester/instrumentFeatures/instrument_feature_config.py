from vwap_price_feature import VwapPriceInstrumentFeature
from position_feature import PositionFeature
from moving_average_feature import MovingAverageInstrumentFeature
from moving_sdev_feature import MovingSDevInstrumentFeature
from exp_moving_average_feature import ExpMovingAverageInstrumentFeature
from macd_feature import MACDInstrumentFeature
from momentum_feature import MomentumInstrumentFeature
from bollinger_bands_feature import BollingerBandsInstrumentFeature
from rsi_feature import RSIInstrumentFeature
from instrument_feature import InstrumentFeature
from backtester.logger import *


featureIdToFeatureCls = {'vwap': VwapPriceInstrumentFeature,
                         'position': PositionFeature,
                         'moving_average': MovingAverageInstrumentFeature,
                         'moving_sdev' : MovingSDevInstrumentFeature,
                         'exponential_moving_average' : ExpMovingAverageInstrumentFeature,
                         'macd' : MACDInstrumentFeature,
                         'momentum' : MomentumInstrumentFeature,
                         'bollinger_bands' : BollingerBandsInstrumentFeature,
                         'rsi' : RSIInstrumentFeature,
                         }

class InstrumentFeatureConfig:

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
    def setupCustomInstrumentFeatures(cls, customFeatureIdToFeatureCls):
        InstrumentFeatureConfig.customFeatureIdToFeatureCls = customFeatureIdToFeatureCls

    @classmethod
    def getClassForInstrumentFeatureId(cls, instrumentFeatureId):
        if instrumentFeatureId in InstrumentFeatureConfig.customFeatureIdToFeatureCls:
            return InstrumentFeatureConfig.customFeatureIdToFeatureCls[instrumentFeatureId]
        if instrumentFeatureId in featureIdToFeatureCls:
            return featureIdToFeatureCls[instrumentFeatureId]
        logError('%s not a valid instrument feature Id. Use a predefined one or provide a custom implementation' % instrumentFeatureId)
        return InstrumentFeature
