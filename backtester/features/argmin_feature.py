from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class ArgMinFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data)<1:
        	return 0
        return data[-featureParams['period']:].idxmin()
