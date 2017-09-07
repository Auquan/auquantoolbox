from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np


class ArgMaxFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        # avg = ma(data, featureParams['period'])
        if len(data) < 1:
            return 0
        return data[-featureParams['period']:].idxmax()
