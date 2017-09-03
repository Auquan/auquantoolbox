from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class Candle2Feature(Feature):

	#This is an implementation of Bearish Marubuzo

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
        return float(np.abs(h-o)+np.abs(c-l))/float(c)
