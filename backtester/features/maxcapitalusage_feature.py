from backtester.features.feature import Feature


class MaxCapitalUsageFeature(Feature):

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
        maxUsage = 0
        capitalUsageDict = instrumentManager.getDataDf()[featureKey]
        capitalKey = 'capital'
        if 'capitalKey' in featureParams:
            capitalKey = featureParams['capitalKey']
        if len(capitalUsageDict) <= 1:
            return 0
        capitalDict = instrumentManager.getDataDf()[capitalKey]
        capital = capitalDict.values[-2]
        capitalUsed = featureParams['initial_capital'] - capital
        maxUsage = capitalUsed if capitalUsed > capitalUsageDict.values[-2] else capitalUsageDict.values[-2]
        return maxUsage
