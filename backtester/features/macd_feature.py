from feature import Feature
from backtester.financial_fn import ma


class MACDFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg1 = ma(data, featureParams['period1'])
        avg2 = ma(data, featureParams['period2'])
        if len(avg1.index) > 0:
            return (avg1 - avg2)[-1]
        else:
            return 0
