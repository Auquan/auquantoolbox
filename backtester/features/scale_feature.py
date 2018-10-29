from backtester.features.feature import *
import pandas as pd
import numpy as np

class ScaleFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(dataDf)
        checkPeriod(featureParams)
        checkScale(featureParams)
        cClean(dataDf)
        data = dataDf[-featureParams['period']:]
        scale = np.abs(data).mul(featureParams['scale']).div(np.abs(data).sum())
        cClean(scale)
        return scale.iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']][-featureParams['period']:]
        checkData(data)
        checkPeriod(featureParams)
        checkScale(featureParams)
        cClean(data)
        scale = np.abs(data).mul(featureParams['scale']).div(np.abs(data).sum()).iloc[-1]
        scale = fClean(scale)
        return scale
