from backtester.features.feature import Feature
import numpy as np


class VwapPriceInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        askVolume = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['askVolume']).iloc[-1]
        bidVolume = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['bidVolume']).iloc[-1]
        askPrice = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['askPrice']).iloc[-1]
        bidPrice = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['bidPrice']).iloc[-1]

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
