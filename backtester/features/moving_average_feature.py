from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MovingAverageFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        if len(data) < 1:
        	return 0
        return avg
