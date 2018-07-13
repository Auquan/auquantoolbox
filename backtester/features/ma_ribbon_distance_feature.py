from backtester.features.feature import Feature
import numpy as np
from scipy import stats
from scipy import spatial
import pandas as pd


class MARibbonDistanceFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        instrumentDict = instrumentManager.getAllInstrumentsByInstrumentId()
        instrumentIds = list(instrumentDict.keys())
        rolling_means = pd.Series([np.zeros(featureParams['numRibbons'])] * len(instrumentDict), index=instrumentIds)

        space = int((featureParams['endPeriod'] - featureParams['startPeriod']) / (featureParams['numRibbons'] - 1))

        collatedData = {}
        for idx in np.linspace(featureParams['startPeriod'], featureParams['endPeriod'], featureParams['numRibbons']):
            i = int(idx)
            collatedData[i] = dataDf[-i:].mean()
            for instrumentId in instrumentIds:
                rolling_means[instrumentId][i / space - 1] = collatedData[i][instrumentId]

        toRtn = {}
        for instrumentId in instrumentIds:
            ranking = stats.rankdata(rolling_means[instrumentId])
            d = spatial.distance.hamming(ranking, range(1, 1 + len(rolling_means[instrumentId])))
            toRtn[instrumentId] = d

        return pd.Series(toRtn, index=instrumentIds)

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        rolling_means = np.zeros(featureParams['numRibbons'])
        if len(data) < 1:
            return rolling_means
        space = int((featureParams['endPeriod'] - featureParams['startPeriod']) / (featureParams['numRibbons'] - 1))
        for idx in np.linspace(featureParams['startPeriod'], featureParams['endPeriod'], featureParams['numRibbons']):
            i = int(idx)
            rolling_means[i / space - 1] = data[-i:].mean()
        ranking = stats.rankdata(rolling_means)
        d = spatial.distance.hamming(ranking, range(1, 1 + len(rolling_means)))
        return d
