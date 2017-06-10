from backtester.logger import *
from backtester.instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from backtester.lookback_data import LookbackData


class Instrument(object):
    def __init__(self, instrumentId, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        featureConfigs = tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        self.__lookbackFeatures = LookbackData(tsParams.getLookbackSize(), map(lambda x: x.getFeatureKey(), featureConfigs))
        self.__position = 0
        self.tsParams = tsParams

    def getInstrumentType(self):
        raise NotImplementedError
        return INSTRUMENT_TYPE_UNDEFINED

    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__currentInstrumentUpdate.getTradeSymbol()

    def getLookbackFeatures(self):
        return self.__lookbackFeatures

    def update(self, instrumentUpdate):
        if (self.__currentInstrumentUpdate is not None) and (instrumentUpdate is not None):
            if self.__currentInstrumentUpdate.getTimeOfUpdate() > instrumentUpdate.getTimeOfUpdate():
                logWarn('Instrument update time is older than current instrument update time')

        self.__currentInstrumentUpdate = instrumentUpdate

    def updatePosition(self, changeInPosition):
        self.__position = self.__position + changeInPosition

    def getCurrentPosition(self):
        return self.__position

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()

    def updateFeatures(self, timeOfUpdate):
        currentFeatures = {}
        featureConfigs = self.tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        for featureConfig in featureConfigs:
            featureKey = featureConfig.getFeatureKey()
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = InstrumentFeatureConfig.getClassForInstrumentFeatureId(featureId)
            featureVal = featureCls.compute(featureParams=featureParams,
                                            featureKey=featureKey,
                                            currentFeatures=currentFeatures,
                                            instrument=self)
            currentFeatures[featureKey] = featureVal
        logInfo('Instrument Features: %s: %s' % (self.__instrumentId, str(currentFeatures)))
        self.__lookbackFeatures.addData(timeOfUpdate, currentFeatures)
