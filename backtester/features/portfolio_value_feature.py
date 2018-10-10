from backtester.features.feature import Feature
from backtester.logger import *

class PortfolioValueFeature(Feature):

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        try:
            return featureParams['initial_capital'] + currentMarketFeatures[featureParams['pnl']]
        except KeyError:
            logError('currentMarketFeatures does not contain pnl Key')
