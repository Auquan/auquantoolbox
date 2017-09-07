from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np


class Candle5Feature(Feature):

	#This checks if both shadows are equal length

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        if 'featureName' in featureParams and 'period' in featureParams:
            data = lookbackDataDf[featureParams['featureName']]
            h = data[-featureParams['period']:].max()
            l = data[-featureParams['period']:].min()
            o = data[-featureParams['period']]
            c = data[-1]
        else:
            h = lookbackDataDf['high'].iloc[-1]
            l = lookbackDataDf['low'].iloc[-1]
            o = lookbackDataDf['open'].iloc[-1]
            c = lookbackDataDf['close'].iloc[-1]
        return np.abs(h-o) == np.abs(c-l)
