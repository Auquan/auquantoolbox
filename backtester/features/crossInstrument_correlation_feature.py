from backtester.features.feature import Feature
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
        if featureParams['period'] == 0:
        		raise ValueError("Period can not be zero")
        if math.isnan(x.rolling(featureParams['period']).corr(y).iloc[-1]):
        		return 0
        return x.rolling(featureParams['period']).corr(y).iloc[-1]
       
