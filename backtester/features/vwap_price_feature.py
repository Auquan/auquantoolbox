from backtester.features.feature import Feature
import numpy as np


class VwapPriceInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        askVolume = instrumentLookbackData.getFeatureDf(featureParams['askVolume']).iloc[-1]
        bidVolume = instrumentLookbackData.getFeatureDf(featureParams['bidVolume']).iloc[-1]
        askPrice = instrumentLookbackData.getFeatureDf(featureParams['askPrice']).iloc[-1]
        bidPrice = instrumentLookbackData.getFeatureDf(featureParams['bidPrice']).iloc[-1]

        totalVolume = (askVolume + bidVolume)
        vwap = ((askPrice * askVolume) + (bidPrice * bidVolume)) / totalVolume

        vwap[vwap == np.Inf] = 0
        return vwap

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
