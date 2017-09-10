from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np

# Correlation between two instruments over some number of data points specified by user.

class MovingCorrelationFeature(Feature):

    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        lookbackInstrumentFeaturesDf = instrument.getDataDf()
        x = lookbackInstrumentFeaturesDf[featureParams['series1']]
        y = lookbackInstrumentFeaturesDf[featureParams['series2']]

        if (len(x) < 1) or (len(y) < 1):
        	return 0
        return round(x.rolling(featureParams['period']).corr(y)[-1], 3)

    @classmethod
    def computeForMarket(cls, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeaturesDf = instrumentManager.getDataDf()
        x = lookbackMarketFeaturesDf[featureParams['series1']]
        y = lookbackMarketFeaturesDf[featureParams['series2']]

        if (len(x) < 1) or (len(y) < 1):
        	return 0
        return round(x.rolling(featureParams['period']).corr(y)[-1], 3)
