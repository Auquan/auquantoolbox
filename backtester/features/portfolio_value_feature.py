from backtester.features.feature import Feature


class PortfolioValueFeature(Feature):

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return featureParams['initial_capital'] + currentMarketFeatures[featureParams['pnl']]
