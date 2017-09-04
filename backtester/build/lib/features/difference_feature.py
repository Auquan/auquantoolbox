from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class DifferenceFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) < featureParams['period'] :
            return 0
        return data[-1] - data[-featureParams['period']]
