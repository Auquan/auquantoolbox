from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MovingAverageFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        #avg = ma(data, featureParams['period'])
        if len(data.index) < featureParams['period'] :
            return currentFeatures[featureParams['featureName']]
        return np.mean(data[-featureParams['period']:])
