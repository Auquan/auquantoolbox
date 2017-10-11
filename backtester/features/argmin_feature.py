from backtester.features.feature import Feature
import pandas as pd


class ArgMinFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        featureDataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        if len(featureDataDf) < 1:
            instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
            zeroSeries = pd.Series([0] * len(instrumentDict), index=instrumentDict.keys())
            return zeroSeries
        return featureDataDf[-featureParams['period']:].idxmin().astype(object)

    '''
    Computing for Market.
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        if len(data) < 1:
            return 0
        return data[-featureParams['period']:].idxmin()
