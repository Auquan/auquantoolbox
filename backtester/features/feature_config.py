from backtester.features.feature import Feature
from backtester.logger import *
from backtester.features.argmax_feature import ArgMaxFeature
from backtester.features.argmin_feature import ArgMinFeature
from backtester.features.bollinger_bands_feature import BollingerBandsFeature
from backtester.features.bollinger_bands_lower_feature import BollingerBandsLowerFeature
from backtester.features.bollinger_bands_upper_feature import BollingerBandsUpperFeature
from backtester.features.capital_feature import CapitalFeature
from backtester.features.crossInstrument_correlation_feature import MovingInstrumentCorrelationFeature
from backtester.features.crossSectionMomentum_feature import CrossSectionMomentumFeature
from backtester.features.delay_feature import DelayFeature
from backtester.features.difference_feature import DifferenceFeature
from backtester.features.direction_feature import DirectionFeature
from backtester.features.exp_moving_average_feature import ExpMovingAverageFeature
from backtester.features.fees_feature import FeesFeature
from backtester.features.macd_feature import MACDFeature
from backtester.features.ma_ribbon_distance_feature import MARibbonDistanceFeature
from backtester.features.momentum_feature import MomentumFeature
from backtester.features.moving_average_feature import MovingAverageFeature
from backtester.features.moving_correlation import MovingCorrelationFeature
from backtester.features.moving_max import MovingMaximumFeature
from backtester.features.moving_min import MovingMinimumFeature
from backtester.features.moving_sdev_feature import MovingSDevFeature
from backtester.features.moving_sum import MovingSumFeature
from backtester.features.portfolio_value_feature import PortfolioValueFeature
from backtester.features.position_instrument_feature import PositionInstrumentFeature
from backtester.features.profitloss_feature import ProfitLossFeature
from backtester.features.rank_feature import RankFeature
from backtester.features.ratio_feature import RatioMarketFeature
from backtester.features.rsi_feature import RSIFeature
from backtester.features.scale_feature import ScaleFeature
from backtester.features.score_fairvalue_feature import ScoreFairValueFeature
from backtester.features.score_logloss_feature import ScoreLogLossFeature
from backtester.features.vwap_price_feature import VwapPriceInstrumentFeature
from backtester.features.score_problem1 import ProblemOneScore
from backtester.features.variance_feature import VarianceFeature
from backtester.features.maxcapitalusage_feature import MaxCapitalUsageFeature
from backtester.features.maxDrawdown_feature import MaxDrawdownFeature
from backtester.features.total_profit_feature import TotalProfitFeature
from backtester.features.total_loss_feature import TotalLossFeature
from backtester.features.count_profit_feature import CountProfitFeature
from backtester.features.count_loss_feature import CountLossFeature

featureIdToFeatureCls = {'argmax': ArgMaxFeature,
                         'argmin': ArgMinFeature,
                         'bollinger_bands': BollingerBandsFeature,
                         'bollinger_bands_lower': BollingerBandsLowerFeature,
                         'bollinger_bands_upper': BollingerBandsUpperFeature,
                         'capital': CapitalFeature,
                         'cross_sectional_momentum': CrossSectionMomentumFeature,
                         'cross_instrument_correlation': MovingInstrumentCorrelationFeature,
                         'delay': DelayFeature,
                         'difference': DifferenceFeature,
                         'direction': DirectionFeature,
                         'exponential_moving_average': ExpMovingAverageFeature,
                         'fees': FeesFeature,
                         'macd': MACDFeature,
                         'ma_ribbon_distance': MARibbonDistanceFeature,
                         'momentum': MomentumFeature,
                         'moving_average': MovingAverageFeature,
                         'moving_correlation': MovingCorrelationFeature,
                         'moving_max': MovingMaximumFeature,
                         'moving_min': MovingMinimumFeature,
                         'moving_sdev': MovingSDevFeature,
                         'moving_sum': MovingSumFeature,
                         'portfolio_value': PortfolioValueFeature,
                         'position': PositionInstrumentFeature,
                         'pnl': ProfitLossFeature,
                         'rank': RankFeature,
                         'ratio': RatioMarketFeature,
                         'rsi': RSIFeature,
                         'scale': ScaleFeature,
                         'score_fv': ScoreFairValueFeature,
                         'score_ll': ScoreLogLossFeature,
                         'vwap': VwapPriceInstrumentFeature,
                         'prob1_score': ProblemOneScore,
                         'total_loss': TotalLossFeature,
                         'total_profit': TotalProfitFeature,
                         'count_loss': CountLossFeature,
                         'count_profit': CountProfitFeature,
                         'maxDrawdown': MaxDrawdownFeature,
                         'variance': VarianceFeature,
                         'maxCapitalUsage': MaxCapitalUsageFeature
                         }


class FeatureConfig:

    customFeatureIdToFeatureCls = {}

    def __init__(self, configDict):
        if 'featureId' not in configDict:
            logError('featureId missing in market feature config dictionary %s', configDict['featureKey'])
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
