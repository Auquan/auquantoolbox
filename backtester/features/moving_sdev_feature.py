from backtester.features.feature import Feature
from backtester.financial_fn import msdev


class MovingSDevFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        sdev = data[-featureParams['period']:].std()
        if len(data) < 1:
            return 0
        return sdev
