from backtester.features.feature import Feature
import pandas as pd


class DifferenceFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if len(dataDf.index) < featureParams['period']:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries
        return dataDf.iloc[-1] - dataDf.iloc[-featureParams['period']]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) < featureParams['period']:
            return 0
        return data[-1] - data[-featureParams['period']]
