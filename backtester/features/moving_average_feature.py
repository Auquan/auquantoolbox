from feature import Feature
from backtester.financial_fn import ma


class MovingAverageFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg = ma(data, featureParams['period'])
        if len(avg.index) > 0:
            return avg[-1]
        else:
            return currentFeatures[featureParams['featureName']]
