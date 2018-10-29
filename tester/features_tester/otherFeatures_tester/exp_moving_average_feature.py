from backtester.features.feature import *
import math
import numpy as np

class ExpMovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        prev_ema = data.iloc[-1]
        print(prev_ema)
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = data['open'].iloc[-1] * alpha + prev_ema['ema'] * (1 - alpha)
        print(avg)
        return np.nan_to_num(avg)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf['open']
        checkData(data)
        checkPeriod(featureParams)
        prev_ema = lookbackDataDf['ema'].iloc[-1]
        print(prev_ema)
        halflife = featureParams['period']
        alpha = 1 - math.exp(math.log(0.5) / halflife)
        avg = data.iloc[-1] * alpha + prev_ema * (1 - alpha)
        if(math.isnan(avg)):
            avg=0
        print(avg)
        return avg
