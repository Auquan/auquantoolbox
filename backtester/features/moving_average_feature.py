from backtester.features.feature import *
from backtester.logger import *
import numpy as np
# Average of feature name over some number of previous data points including current.
# number of data points specified by user


class MovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        avg = data[-featureParams['period']:].mean()
        pClean(avg)
        return avg

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        infToNan(data)
        avg = data[-featureParams['period']:].mean()
        avg = np.nan_to_num(avg)
        if len(data) < 1:
            return 0
        return avg
