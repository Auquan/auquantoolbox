from backtester.features.feature import Feature
import numpy as np


class FeesFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getDataForFeatureForAllInstruments('position')
        feesDict = featureParams['feesDict']
        currentPosition = positionData.iloc[-1]
        previousPosition = 0 if updateNum < 2 else positionData.iloc[-2]
        changeInPosition = currentPosition - previousPosition
        print currentPosition
        print previousPosition
        fees = np.abs(changeInPosition) * [feesDict[np.sign(x)] for x in changeInPosition]
        return fees

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        raise NotImplementedError
        return None
