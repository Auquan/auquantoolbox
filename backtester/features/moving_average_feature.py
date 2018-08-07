from backtester.features.feature import Feature
from backtester.logger import *
import numpy as np
# Average of feature name over some number of previous data points including current.
# number of data points specified by user


class MovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        data.replace(np.Inf, np.nan, inplace = True)
        data.replace(-np.Inf, np.nan, inplace = True)
        avg = data[-featureParams['period']:].mean()
        avg.fillna(0, inplace = True)
        return avg

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        data.replace(np.Inf, np.nan, inplace = True)
        data.replace(-np.Inf, np.nan, inplace = True)
        avg = data[-featureParams['period']:].mean()
        avg = np.nan_to_num(avg)
        if len(data) < 1:
            return 0
        return avg

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty :
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        movingAvg = data.rolling(window=featureParams['period'], min_periods=1).mean()
        movingAvg.fillna(0, inplace = True)
        return movingAvg
