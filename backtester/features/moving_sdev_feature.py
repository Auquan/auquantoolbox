from feature import Feature
from backtester.financial_fn import msdev


class MovingSDevFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        sdev = msdev(data, featureParams['period'])
        if len(sdev.index) > 0:
            return sdev[-1]
        else:
            return 0
