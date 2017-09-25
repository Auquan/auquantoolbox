from backtester.features.feature import Feature
import numpy as np


class ScaleFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        dataDf = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        data = dataDf[-featureParams['period']:]
        return data.mul(featureParams['scale']).div(np.abs(data).sum()).iloc[-1]

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']][-featureParams['period']:]
        return data.mul(featureParams['scale']).div(np.abs(data).sum()).iloc[-1]
