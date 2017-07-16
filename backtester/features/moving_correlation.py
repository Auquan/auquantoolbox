from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MovingCorrelationFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        x = lookbackDataDf[featureParams['series1']]
        y = lookbackDataDf[featureParams['series2']]
        #avg = ma(data, featureParams['period'])
        return x.rolling(featureParams['period']).corr(y)[-1]
