from backtester.features.feature import Feature
import numpy as np


class VwapPriceInstrumentFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        askVolume = instrumentLookbackData.getFeatureDf(featureParams['askVolume'])
        if askVolume is None or askVolume.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        bidVolume = instrumentLookbackData.getFeatureDf(featureParams['bidVolume'])
        if bidVolume is None or bidVolume.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        askPrice = instrumentLookbackData.getFeatureDf(featureParams['askPrice'])
        if askPrice is None or askPrice.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        bidPrice = instrumentLookbackData.getFeatureDf(featureParams['bidPrice'])
        if bidPrice is None or bidPrice.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None

        totalVolume = (askVolume + bidVolume)
        vwap = ((askPrice * askVolume) + (bidPrice * bidVolume)) / totalVolume
        vwap.replace(np.Inf,np.nan, inplace=True)
        vwap.replace(-np.Inf,np.nan,inplace=True)
        vwap.fillna(0,inplace=True)
        return vwap.iloc[-1]

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        askVolume = featureManager.getFeatureDf(featureParams['askVolume'])
        if askVolume is None or askVolume.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        bidVolume = featureManager.getFeatureDf(featureParams['bidVolume'])
        if bidVolume is None or bidVolume.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        askPrice = featureManager.getFeatureDf(featureParams['askPrice'])
        if askPrice is None or askPrice.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        bidPrice = featureManager.getFeatureDf(featureParams['bidPrice'])
        if bidPrice is None or bidPrice.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        totalVolume = (askVolume + bidVolume)
        vwap = ((askPrice * askVolume) + (bidPrice * bidVolume)) / totalVolume
        vwap.replace(np.Inf,np.nan, inplace=True)
        vwap.replace(-np.Inf,np.nan,inplace=True)
        vwap.fillna(0,inplace=True)
        return vwap
