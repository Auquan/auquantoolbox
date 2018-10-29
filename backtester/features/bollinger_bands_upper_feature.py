from backtester.features.feature import *
from backtester.financial_fn import ma
from backtester.financial_fn import msdev
import numpy as np


class BollingerBandsUpperFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        avg = data[-featureParams['period']:].mean().fillna(0)
        sdev = data[-featureParams['period']:].std().fillna(0)
        return avg + sdev

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std()
        return np.nan_to_num(avg) + np.nan_to_num(sdev)
