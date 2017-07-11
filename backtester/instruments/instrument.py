from backtester.logger import *
from backtester.features.feature_config import FeatureConfig
from backtester.lookback_data import LookbackData
import copy


def getCompulsoryInstrumentFeatureConfigs(tsParams):
    positionConfigDict = {'featureKey': 'position',
                          'featureId': 'position',
                          'params': {}}
    feesConfigDict = {'featureKey': 'fees',
                      'featureId': 'fees',
                      'params': {'price': 'close',
                                 'feesDict': {-1: 0.001, 1: 0.001, 0: 0}}}
    profitlossConfigDict = {'featureKey': 'pnl',
                            'featureId': 'pnl',
                            'params': {'price': tsParams.getPriceFeatureKey(),
                                       'fees': 'fees'}}
    capitalConfigDict = {'featureKey': 'capital',
                         'featureId': 'capital',
                         'params': {'price': tsParams.getPriceFeatureKey(), 'fees': 'fees'}}
    compulsoryConfigDicts = [positionConfigDict, feesConfigDict, profitlossConfigDict, capitalConfigDict]
    compulsoryInstrumentFeatureConfigs = map(lambda x: FeatureConfig(x), compulsoryConfigDicts)
    return compulsoryInstrumentFeatureConfigs


class Instrument(object):
    def __init__(self, instrumentId, bookDataFeatures, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        self.tsParams = tsParams
        self.__position = 0
        self.__compulsoryFeatureConfigs = getCompulsoryInstrumentFeatureConfigs(tsParams)
        featureConfigs = tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        compulsoryFeatureColumns = map(lambda x: x.getFeatureKey(), self.__compulsoryFeatureConfigs)
        featureColumns = map(lambda x: x.getFeatureKey(), featureConfigs)
        self.__lookbackFeatures = LookbackData(tsParams.getLookbackSize(), bookDataFeatures + featureColumns + compulsoryFeatureColumns)

    def getInstrumentType(self):
        raise NotImplementedError
        return INSTRUMENT_TYPE_UNDEFINED

    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__currentInstrumentUpdate.getTradeSymbol()

    def getDataDf(self):
        return self.__lookbackFeatures.getData()

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
        currentFeatures = copy.deepcopy(self.getCurrentBookData())
        featureConfigs = self.tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        featureConfigs = featureConfigs + self.__compulsoryFeatureConfigs
        for featureConfig in featureConfigs:
            featureKey = featureConfig.getFeatureKey()
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
            featureVal = featureCls.computeForInstrument(featureParams=featureParams,
                                                         featureKey=featureKey,
                                                         currentFeatures=currentFeatures,
                                                         instrument=self,
                                                         instrumentManager=None)  # TODO
            currentFeatures[featureKey] = featureVal
        logInfo('Instrument Features: %s: %s' % (self.__instrumentId, str(currentFeatures)))
        self.__lookbackFeatures.addData(timeOfUpdate, currentFeatures)
