from logger import *
from instrumentFeatures import *
from lookback_data import LookbackData


class Instrument:
    def __init__(self, instrumentId, startingInstrumentUpdate):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = startingInstrumentUpdate
        self.__lookbackFeatures = LookbackData()

    def getInstrumentId(self):
        return self.__instrumentId

    def update(self, instrumentUpdate):
        if (self.__currentInstrumentUpdate is not None) and (instrumentUpdate is not None):
            if self.__currentInstrumentUpdate.getTimeOfUpdate() > instrumentUpdate.getTimeOfUpdate():
                logWarn('Instrument update time is older than current instrument update time')

        self.__currentInstrumentUpdate = instrumentUpdate

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()

    def updateFeatures(self, timeOfUpdate):
        currentFeatures = {}
        for instrumentFeatureIdentifier in instrumentFeatureIdentifiers:
            featureVal = InstrumentFeature.computeForFeature(instrumentFeatureIdentifier, self.getCurrentBookData(), currentFeatures)
            currentFeatures[instrumentFeatureIdentifier] = featureVal
        self.__lookbackFeatures.addData(currentFeatures)
