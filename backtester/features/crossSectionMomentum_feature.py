from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class CrossSectionMomentumFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        #avg = ma(data, )
        R = (data / data.shift(featureParams['period']))
    	ranks = (R.T - R.T.mean()).T.mean()
    	return ranks

