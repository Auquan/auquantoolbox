from backtester.features.feature import Feature

class CountFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureKey]
        if len(data) <= 1:
            return 0
        return data.iloc[-2]+1
