from backtester.features.feature import *


class VwapPriceInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        askVolume = instrumentLookbackData.getFeatureDf(featureParams['askVolume'])
        bidVolume = instrumentLookbackData.getFeatureDf(featureParams['bidVolume'])
        askPrice = instrumentLookbackData.getFeatureDf(featureParams['askPrice'])
        bidPrice = instrumentLookbackData.getFeatureDf(featureParams['bidPrice'])
        checkVwapData(askVolume, bidVolume, askPrice, bidPrice)
        totalVolume = (askVolume + bidVolume)
        vwap = ((askPrice * askVolume) + (bidPrice * bidVolume)) / totalVolume
        cClean(vwap)
        return vwap.iloc[-1]

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
