from logger import *
from instrumentFeatures import *
from lookback_data import LookbackData


class Instrument:
    def __init__(self, instrumentId, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        self.__lookbackFeatures = LookbackData()
        self.tsParams = tsParams

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

    def updateFeatures(self, timeOfUpdate):
        currentFeatures = {}
        featureConfigs = self.tsParams.getFeatureIdentifiersForInstrumentType(self.getInstrumentType())
        for featureConfig in featureConfigs:
            featureId = featureConfig.getFeatureId()
            featureParams = featureConfig.getFeatureParams()
            featureVal = InstrumentFeature.computeForFeature(instrumentFeatureId=featureId,
                                                             featureParams=featureParams,
                                                             currentFeatures=currentFeatures,
                                                             instrument=self)
            currentFeatures[featureConfig.getFeatureKey()] = featureVal
        self.__lookbackFeatures.addData(currentFeatures)
