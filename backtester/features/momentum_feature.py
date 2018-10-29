from backtester.features.feature import *
import pandas as pd

class MomentumFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        checkData(data)
        checkPeriod(featureParams)
        mid = data.shift(featureParams['period']).fillna(method='pad')
        if len(data.index) > featureParams['period']:
            momentum = ((data.iloc[-1] / mid.iloc[-1]) - 1) * 100
            cClean(momentum)
            return momentum
        else:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        checkData(data)
        checkPeriod(featureParams)
        mid = data.shift(featureParams['period']).fillna(method='pad')
        if len(data.index) > featureParams['period']:
            m = ((data.iloc[-1] /mid.iloc[-1]) -1)
        else:
            m = 0
        fClean(m)
        return m*100
