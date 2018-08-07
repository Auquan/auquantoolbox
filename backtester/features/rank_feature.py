from backtester.features.feature import Feature
import pandas as pd
import numpy as np

class RankFeature(Feature):

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
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        rank = data[-featureParams['period']:].rank(pct=True).iloc[-1]
        return rank

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
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        rank = data[-featureParams['period']:].rank(pct=True).iloc[-1]
        return rank

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None or data.empty:
            raise ValueError('data cannot be null')
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        if featureParams['period']==0:
            raise ValueError('period cannot be 0')
            return None
        data.replace(np.Inf,np.nan, inplace=True)
        data.replace(-np.Inf,np.nan,inplace=True)
        data.fillna(0,inplace=True)
        pctrank = lambda x: pd.Series(x).rank(pct=True).iloc[-1]
        rank = data.rolling(window=featureParams['period'], min_periods=1).apply(pctrank)
        return rank
