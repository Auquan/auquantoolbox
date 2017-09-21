from backtester.features.feature import Feature
from backtester.financial_fn import ma
import numpy as np
import pandas as pd


class CrossSectionMomentumFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):      
        raise NotImplementedError
        return None

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        data = {}
        if 'instrumentIds' in featureParams:
            allInstruments = featureParams['instrumentIds']
        else:
            allInstruments = instrumentManager.getAllInstrumentsByInstrumentId()
        for instrumentId in allInstruments:
            instrument = allInstruments[instrumentId]
            data[instrumentId] = instrument.getDataDf()[featureParams['featureName']]
        df = pd.DataFrame(data)
        R = (df / df.shift(featureParams['period']))
        ranks = (R.T - R.T.mean()).T.mean()
        return ranks

