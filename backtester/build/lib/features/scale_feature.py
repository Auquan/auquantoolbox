from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class ScaleFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']][-featureParams['period']:]
    	return data.mul(featureParams['scale']).div(np.abs(data).sum())
