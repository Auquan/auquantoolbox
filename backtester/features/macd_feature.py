from backtester.features.feature import Feature
from backtester.financial_fn import ma


class MACDFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg1 = data[-featureParams['period1']:].mean()
        avg2 = data[-featureParams['period2']:].mean()
        if len(data) < 1:
        	return 0
        return (avg1 - avg2)
