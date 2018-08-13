from backtester.features.feature import *
import pandas as pd

class RankFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        rank = data[-featureParams['period']:].rank(pct=True).iloc[-1]
        return rank

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        rank = data[-featureParams['period']:].rank(pct=True).iloc[-1]
        return rank

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        cClean(data)
        pctrank = lambda x: pd.Series(x).rank(pct=True).iloc[-1]
        rank = data.rolling(window=featureParams['period'], min_periods=1).apply(pctrank)
        return rank
