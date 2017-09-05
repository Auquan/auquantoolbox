from backtester.features.feature import Feature

class CountFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureKey].iloc[-1]
        return data+1

