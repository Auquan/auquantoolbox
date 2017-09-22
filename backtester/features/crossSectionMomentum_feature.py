from backtester.features.feature import Feature
import pandas as pd


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
        R = (df / df.shift(featureParams['period']))
        ranks = (R.T - R.T.mean()).T.mean()
        return ranks
