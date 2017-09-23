from backtester.features.feature import Feature


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
