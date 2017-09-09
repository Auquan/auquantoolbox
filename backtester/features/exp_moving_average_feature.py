from backtester.features.feature import Feature
import math


class ExpMovingAverageFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureKey]
        if len(data.index) > 0:
            prev_ema = data[-1]
        else:
            prev_ema = currentFeatures[featureParams['featureName']]
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = currentFeatures[featureParams['featureName']] * alpha + prev_ema * (1 - alpha)
        return avg
