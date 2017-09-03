from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MARibbonHammingDistanceFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        rolling_means = np.zeros(featureParams['numRibbons'])
        if len(data) < 1:
        	return rolling_means
        space = int((featureParams['endPeriod'] - featureParams['startPeriod'])/(featureParams['numRibbons']-1))
        for idx in np.linspace(featureParams['startPeriod'], featureParams['endPeriod'], featureParams['numRibbons']):
            i = int(idx)
            rolling_means[i/space - 1] = data[-i:].mean()
        ranking = stats.rankdata(rolling_means)
        d = distance.hamming(ranking, range(1, 1+len(rolling_means)))
        return d
