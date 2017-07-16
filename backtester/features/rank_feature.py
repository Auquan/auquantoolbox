from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class RankFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
    	return data[-featureParams['period']:].rank(axis=1, pct=True)
