from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np

# Average of feature name over some number of previous data points including current.
# number of data points specified by user

class MovingAverageFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        if len(data) < 1:
        	return 0
        return avg
