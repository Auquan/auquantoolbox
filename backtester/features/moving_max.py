from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MovingMaximumFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        #avg = ma(data, featureParams['period'])
        return data.rolling(featureParams['period']).apply(np.argmax) + 1
