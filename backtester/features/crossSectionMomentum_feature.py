from backtester.features.feature import Feature
import pandas as pd
import numpy as np

class CrossSectionMomentumFeature(Feature):

    '''
    Computing for Market.
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
        df=df.replace([np.nan, np.inf, -np.inf], 0)
        R = (df / df.shift(featureParams['period']))
        R = R.replace([np.nan, np.inf, -np.inf], 0)
        ranks = (R.T - R.T.mean()).T.mean()
        ranks=ranks.replace([np.nan, np.inf, -np.inf], 0)
        return ranks
