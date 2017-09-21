from backtester.features.feature import Feature


class RatioMarketFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        feature1 = featureParams['featureName1']
        feature2 = featureParams['featureName2']
        if (instrument):
            return 0
        lookbackData = instrument.getDataDf()
        if len(lookbackData) < 1:
            return 1
        feature1 = lookbackData[featureParams['featureName1']].iloc[-1]
        feature2 = lookbackData[featureParams['featureName2']].iloc[-1]
        if feature2 == 0:
            return 0
        return feature2 / float(feature1)

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        feature = featureParams['featureName']
        instrumentId1 = featureParams['instrumentId1']
        instrument1 = instrumentManager.getInstrument(instrumentId1)
        instrumentId2 = featureParams['instrumentId2']
        instrument2 = instrumentManager.getInstrument(instrumentId2)
        if (instrument1 is None) or (instrument2 is None):
            return 0
        else:
            instrument1Price = instrument1.getDataDf()[feature].iloc[-1]
            instrument2Price = instrument2.getDataDf()[feature].iloc[-1]
            if instrument2Price == 0:
                return 0
            return instrument1Price / float(instrument2Price)
