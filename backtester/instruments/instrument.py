from backtester.logger import *
from backtester.instrumentFeatures.instrument_feature import InstrumentFeature
from backtester.lookback_data import LookbackData


class Instrument(object):
    def __init__(self, instrumentId, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        featureConfigs = tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        self.__lookbackFeatures = LookbackData(500, map(lambda x: x.getFeatureKey(), featureConfigs))
        self.__position = 0
        self.tsParams = tsParams

    def getInstrumentType(self):
        raise NotImplementedError
        return INSTRUMENT_TYPE_UNDEFINED

    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__currentInstrumentUpdate.getTradeSymbol()

    def update(self, instrumentUpdate):
        if (self.__currentInstrumentUpdate is not None) and (instrumentUpdate is not None):
            if self.__currentInstrumentUpdate.getTimeOfUpdate() > instrumentUpdate.getTimeOfUpdate():
                logWarn('Instrument update time is older than current instrument update time')

        self.__currentInstrumentUpdate = instrumentUpdate

    def updatePosition(self, changeInPosition):
        self.__position = self.__position + changeInPosition

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()

    def updateFeatures(self, timeOfUpdate):
        currentFeatures = {}
        featureConfigs = self.tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        for featureConfig in featureConfigs:
            featureId = featureConfig.getFeatureId()
            featureParams = featureConfig.getFeatureParams()
            featureVal = InstrumentFeature.computeForFeature(instrumentFeatureId=featureId,
                                                             featureParams=featureParams,
                                                             currentFeatures=currentFeatures,
                                                             instrument=self)
            currentFeatures[featureConfig.getFeatureKey()] = featureVal
        self.__lookbackFeatures.addData(timeOfUpdate, currentFeatures)
