from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np


class Candle3Feature(Feature):

	#This checks the length of candle realbody

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        if 'featureName' in featureParams and 'period' in featureParams:
        	data = lookbackDataDf[featureParams['featureName']]
        	o = data[-featureParams['period']]
        	c = data[-1]
        else:
        	o = lookbackDataDf['open'].iloc[-1]
        	c = lookbackDataDf['close'].iloc[-1]
        return np.abs(c-o)/float(c)
