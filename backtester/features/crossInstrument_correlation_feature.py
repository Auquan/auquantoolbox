from backtester.features.feature import Feature


class MovingInstrumentCorrelationFeature(Feature):

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['featureName']
        instrumentId1 = featureParams['instrumentId1']
        instrument1 = instrumentManager.getInstrument(instrumentId1)
        instrumentId2 = featureParams['instrumentId2']
        instrument2 = instrumentManager.getInstrument(instrumentId2)
        if (instrument1 is None) or (instrument2 is None):
            return 0
        else:
            x = instrument1.getDataDf()[feature]
            y = instrument2.getDataDf()[feature]

        if (len(x) < 1) or (len(y) < 1):
            return 0
        return x.rolling(featureParams['period']).corr(y)[-1]
