from backtester.features.feature import Feature
from backtester.logger import *
import numpy as np
import math

class MovingInstrumentCorrelationFeature(Feature):

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['featureName']
        instrumentId1 = featureParams['instrumentId1']
        instrumentId2 = featureParams['instrumentId2']
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        df = lookbackInstrumentFeatures.getFeatureDf(feature)
        df = df.replace([np.nan, np.inf, -np.inf], 0)
        x = df[instrumentId1]
        y = df[instrumentId2]
        if (len(x) < 1) or (len(y) < 1):
            return 0
        if featureParams["period"] > max(len(x),len(y)):
            logError("The period is too large")
            return 0
        if featureParams["period"]==0:
            logError("The period can't be zero")
            return 0
        if math.isnan(x.rolling(featureParams['period']).corr(y).iloc[-1]):
        	return 0
        return x.rolling(featureParams['period']).corr(y).iloc[-1]
