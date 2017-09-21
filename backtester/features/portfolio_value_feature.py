from backtester.features.feature import Feature
import numpy as np

class PortfolioValueFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):      
        raise NotImplementedError
        return None


    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return featureParams['initial_capital'] + currentMarketFeatures[featureParams['pnl']]
