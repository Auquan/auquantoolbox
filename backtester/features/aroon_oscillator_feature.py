from backtester.features.feature import *
import numpy as np
import pandas as pd

class AroonOscillatorFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        if len(data) < 1:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries
        data = data.drop_index(drop = True)
        mid1 = (data[-featureParams['period']:].idxmax()).add(1)
        aup = (mid1.div(featureParams['period'])).mul(100)
        mid2 = (data[-featureParams['period']:].idxmin()).add(1)
        adown = (mid2.div(featureParams['period'])).mul(100)
        return aup-adown

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        if len(data) < 1:
            return 0
        data = data.drop_index(drop = True)
        mid1 = (data[-featureParams['period']:].idxmax()).add(1)
        aup = (mid1.div(featureParams['period'])).mul(100)
        mid2 = (data[-featureParams['period']:].idxmin()).add(1)
        adown = (mid2.div(featureParams['period'])).mul(100)
        return aup-adown

    @classmethod
    def computeForInstrumentData(cls, updateNum, featureParams, featureKey, featureManager):
        data = featureManager.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        argMax = data.rolling(window=featureParams['period'], min_periods=1).apply(np.argmax)
        aup = ((argMax.add(1)).div(featureParams['period'])).mul(100)
        argMin = data.rolling(window=featureParams['period'], min_periods=1).apply(np.argmin)
        adown = ((argMin.add(1)).div(featureParams['period'])).mul(100)
        return aup-adown
