from feature import Feature
from backtester.logger import *
from bollinger_bands_feature import BollingerBandsFeature
from exp_moving_average_feature import ExpMovingAverageFeature
from macd_feature import MACDFeature
from momentum_feature import MomentumFeature
from moving_average_feature import MovingAverageFeature
from moving_sdev_feature import MovingSDevFeature
from position_instrument_feature import PositionInstrumentFeature
from ratio_feature import RatioMarketFeature
from rsi_feature import RSIFeature
from vwap_price_feature import VwapPriceInstrumentFeature
from profitloss_feature import  ProfitLossFeature
from fees_feature import  FeesFeature
from capital_feature import CapitalFeature
from portfolio_value_feature import PortfolioValueFeature

featureIdToFeatureCls = {'bollinger_bands': BollingerBandsFeature,
                         'exponential_moving_average': ExpMovingAverageFeature,
                         'fees' : FeesFeature, 
                         'macd': MACDFeature,
                         'momentum': MomentumFeature,
                         'moving_average': MovingAverageFeature,
                         'moving_sdev': MovingSDevFeature,
                         'position': PositionInstrumentFeature,
                         'pnl' :  ProfitLossFeature,
                         'ratio': RatioMarketFeature,
                         'rsi': RSIFeature,
                         'vwap': VwapPriceInstrumentFeature,
                         'capital' : CapitalFeature,
                         'portfolio_value' : PortfolioValueFeature
                         }


class FeatureConfig:

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
    def setupCustomFeatures(cls, customFeatureIdToFeatureCls):
        FeatureConfig.customFeatureIdToFeatureCls = customFeatureIdToFeatureCls

    @classmethod
    def getClassForFeatureId(cls, featureId):
        if featureId in FeatureConfig.customFeatureIdToFeatureCls:
            return FeatureConfig.customFeatureIdToFeatureCls[featureId]
        if featureId in featureIdToFeatureCls:
            return featureIdToFeatureCls[featureId]
        logError('%s not a valid feature Id. Use a predefined one or provide a custom implementation' % featureId)
        return Feature
