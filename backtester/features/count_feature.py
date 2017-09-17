from backtester.features.feature import Feature


class CountFeature(Feature):

    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureKey]
        if len(data.index) < 1:
            return 0
        return data.iloc[-1] + 1
