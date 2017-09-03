from feature import Feature
from backtester.logger import *
from argmax_feature import ArgMaxFeature
from argmin_feature import ArgMinFeature
from bollinger_bands_feature import BollingerBandsFeature
from capital_feature import CapitalFeature
from crossInstrument_correlation_feature import MovingInstrumentCorrelationFeature
from crossSectionMomentum_feature import CrossSectionMomentumFeature
from delay_feature import DelayFeature
from difference_feature import DifferenceFeature
from exp_moving_average_feature import ExpMovingAverageFeature
from fees_feature import  FeesFeature
from macd_feature import MACDFeature
from ma_ribbon_feature import MARibbonHammingDistanceFeature
from momentum_feature import MomentumFeature
from moving_average_feature import MovingAverageFeature
from moving_correlation import MovingCorrelationFeature
from moving_max import MovingMaximumFeature
from moving_min import MovingMinimumFeature
from moving_sdev_feature import MovingSDevFeature
from moving_sum import MovingSumFeature
from portfolio_value_feature import PortfolioValueFeature
from position_instrument_feature import PositionInstrumentFeature
from profitloss_feature import  ProfitLossFeature
from rank_feature import RankFeature
from ratio_feature import RatioMarketFeature
from rsi_feature import RSIFeature
from scale_feature import ScaleFeature
from vwap_price_feature import VwapPriceInstrumentFeature


featureIdToFeatureCls = {'argmax' : ArgMaxFeature,
                         'argmin' : ArgMinFeature,
                         'bollinger_bands': BollingerBandsFeature,
                         'capital' : CapitalFeature,
                         'cross_sectional_momentum' : CrossSectionMomentumFeature,
                         'cross_instrument_correlation' : MovingInstrumentCorrelationFeature,
                         'delay' : DelayFeature,
                         'difference' : DifferenceFeature,
                         'exponential_moving_average': ExpMovingAverageFeature,
                         'fees' : FeesFeature, 
                         'macd': MACDFeature,
                         'ma_ribbon_hammingdistance': MARibbonHammingDistanceFeature,
                         'momentum': MomentumFeature,
                         'moving_average': MovingAverageFeature,
                         'moving_correlation': MovingCorrelationFeature,
                         'moving_max': MovingMaximumFeature,
                         'moving_min': MovingMinimumFeature,
                         'moving_sdev': MovingSDevFeature,
                         'moving_sum' : MovingSumFeature,
                         'portfolio_value' : PortfolioValueFeature,
                         'position': PositionInstrumentFeature,
                         'pnl' :  ProfitLossFeature,
                         'rank' : RankFeature,
                         'ratio': RatioMarketFeature,
                         'rsi': RSIFeature,
                         'scale' : ScaleFeature,
                         'vwap': VwapPriceInstrumentFeature,
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
