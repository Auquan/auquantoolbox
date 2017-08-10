from feature import Feature
from backtester.financial_fn import ma
import numpy as np


class MARibbonFeature(Feature):

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
        
        return rolling_means
