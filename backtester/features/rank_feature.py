from backtester.features.feature import Feature
import pandas as pd


class RankFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        return dataDf[-featureParams['period']:].rank(pct=False).iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        return data[-featureParams['period']:].rank(pct=False).iloc[-1]

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        if data is None:
            logWarn("[%d] instrument data for \"%s\" is not available, can't calculate \"%s\"" % (updateNum, featureParams['featureName'], featureKey))
            return None
        pctrank = lambda x: pd.Series(x).rank(pct=True).iloc[-1]
        rank = data.rolling(window=featureParams['period'], min_periods=1).apply(pctrank)
        return rank
