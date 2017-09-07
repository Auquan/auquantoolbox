from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np


class DelayFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) < featureParams['period'] :
            return 0
        return data[-featureParams['period']]