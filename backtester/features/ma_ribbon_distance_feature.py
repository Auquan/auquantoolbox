from backtester.features.feature import Feature
import numpy as np
from scipy import stats
from scipy import spatial


class MARibbonDistanceFeature(Feature):

    '''
    Computing for Instrument.
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getDataForFeatureForAllInstruments(featureParams['featureName'])
        # TODO KANAV
        raise NotImplementedError

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

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
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
