from logger import *
from instrumentFeatures import *
from lookback_data import LookbackData


class Instrument:
    def __init__(self, instrumentId):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        self.__lookbackFeatures = LookbackData()

    def getInstrumentType(self):
        raise NotImplementedError
        return INSTRUMENT_TYPE_UNDEFINED

    def getInstrumentId(self):
        return self.__instrumentId

    def update(self, instrumentUpdate):
        if (self.__currentInstrumentUpdate is not None) and (instrumentUpdate is not None):
            if self.__currentInstrumentUpdate.getTimeOfUpdate() > instrumentUpdate.getTimeOfUpdate():
                logWarn('Instrument update time is older than current instrument update time')

        self.__currentInstrumentUpdate = instrumentUpdate

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()

    def updateFeatures(self, timeOfUpdate, tsParams):
        currentFeatures = {}
        instrumentFeatureIdentifiers = tsParams.getFeatureIdentifiersForInstrumentType(self.getInstrumentType())
        for instrumentFeatureIdentifier in instrumentFeatureIdentifiers:
            featureKey, featureVal = InstrumentFeature.computeForFeature(instrumentFeatureIdentifier, self.getCurrentBookData(), currentFeatures)
            currentFeatures[featureKey] = featureVal
        self.__lookbackFeatures.addData(currentFeatures)
