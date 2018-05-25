from backtester.features.feature import Feature
import numpy as np
from backtester.logger import *


class FeesFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getFeatureDf('position')
        feesDict = featureParams['feesDict']
        currentPosition = positionData.iloc[-1]
        previousPosition = 0 if updateNum < 2 else positionData.iloc[-2]
        changeInPosition = currentPosition - previousPosition
        fees = np.abs(changeInPosition) * [feesDict[np.sign(x)] for x in changeInPosition]
        if 'price' in featureParams:
            try:
                priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
                currentPrice = priceData.iloc[-1]
            except KeyError:
                currentPrice = 0
            fees = fees * currentPrice
        return fees

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return None
