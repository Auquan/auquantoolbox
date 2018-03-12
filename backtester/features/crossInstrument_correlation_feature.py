from backtester.features.feature import Feature


class MovingInstrumentCorrelationFeature(Feature):

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['featureName']
        instrumentId1 = featureParams['instrumentId1']
        instrumentId2 = featureParams['instrumentId2']
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        df = lookbackInstrumentFeatures.getFeatureDf(feature)

        x = df[instrumentId1]
        y = df[instrumentId2]

        if (len(x) < 1) or (len(y) < 1):
            return 0
        return x.rolling(featureParams['period']).corr(y)[-1]
