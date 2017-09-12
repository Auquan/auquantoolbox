from backtester.logger import *
from backtester.features.feature_config import FeatureConfig
from backtester.lookback_data import LookbackData
from backtester.constants import *
import copy
from itertools import chain


def getCompulsoryInstrumentFeatureConfigs(tsParams, instrumentType):
    positionConfigDict = {'featureKey': 'position',
                          'featureId': 'position',
                          'params': {}}
    feesConfigDict = {INSTRUMENT_TYPE_STOCK: {'featureKey': 'fees',
                                              'featureId': 'fees',
                                              'params': {'price': tsParams.getPriceFeatureKey(),
                                                         'feesDict': {1: 0.05, -1: 0.05, 0: 0}}},
                      INSTRUMENT_TYPE_FUTURE: {'featureKey': 'fees',
                                               'featureId': 'fees',
                                               'params': {'price': tsParams.getPriceFeatureKey(),
                                                          'feesDict': {1: 0.00002392, -1: 0.00012392, 0: 0}}},
                      INSTRUMENT_TYPE_OPTION: {'featureKey': 'fees',
                                               'featureId': 'fees',
                                               'params': {'price': tsParams.getPriceFeatureKey(),
                                                          'feesDict': {1: 0.0005915, -1: 0.0010915, 0: 0}}}}
    profitlossConfigDict = {'featureKey': 'pnl',
                            'featureId': 'pnl',
                            'params': {'price': tsParams.getPriceFeatureKey(),
                                       'fees': 'fees'}}
    capitalConfigDict = {'featureKey': 'capital',
                         'featureId': 'capital',
                         'params': {'price': tsParams.getPriceFeatureKey(), 'fees': 'fees'}}
    varianceConfigDict = {'featureKey': 'variance',
                          'featureId': 'variance',
                          'params': {'pnlKey': 'pnl',
                                     'countKey': 'count'}}
    profitlossRatioConfigDict = {'featureKey': 'pl_ratio',
                                 'featureId': 'pl_ratio',
                                 'params': {'pnlKey': 'pnl',
                                            'countKey': 'count'}}
    compulsoryConfigDicts = [positionConfigDict, feesConfigDict[instrumentType], profitlossConfigDict, capitalConfigDict,
                             varianceConfigDict, profitlossRatioConfigDict]
    compulsoryInstrumentFeatureConfigs = map(lambda x: FeatureConfig(x), compulsoryConfigDicts)
    return compulsoryInstrumentFeatureConfigs


class Instrument(object):

    def __init__(self, instrumentId, bookDataFeatures, tsParams):
        self.__instrumentId = instrumentId
        self.__currentInstrumentUpdate = None
        self.tsParams = tsParams
        self.__position = 0
        self.__lastTradePrice = 0
        self.__compulsoryFeatureConfigs = getCompulsoryInstrumentFeatureConfigs(tsParams, self.getInstrumentType())
        featureConfigs = tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        compulsoryFeatureColumns = map(lambda x: x.getFeatureKey(), self.__compulsoryFeatureConfigs)
        featureColumns = map(lambda x: x.getFeatureKey(), featureConfigs)
        self.__lookbackFeatures = LookbackData(tsParams.getLookbackSize(), list(chain(bookDataFeatures, featureColumns, compulsoryFeatureColumns)))

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

    def updatePositionAtPrice(self, changeInPosition, tradePrice):
        self.__position = self.__position + changeInPosition
        self.__lastTradePrice = tradePrice

    def getCurrentPosition(self):
        return self.__position

    def getLastTradePrice(self):
        return self.__lastTradePrice

    def getCurrentBookData(self):
        return self.__currentInstrumentUpdate.getBookData()

    def updateFeatures(self, timeOfUpdate, instrumentManger):
        currentFeatures = copy.deepcopy(self.getCurrentBookData())
        self.__lookbackFeatures.addData(timeOfUpdate, currentFeatures)
        featureConfigs = self.tsParams.getFeatureConfigsForInstrumentType(self.getInstrumentType())
        featureConfigs = list(chain(featureConfigs, self.__compulsoryFeatureConfigs))
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
                                                         instrumentManager=instrumentManger)
            currentFeatures[featureKey] = featureVal
            self.__lookbackFeatures.addFeatureVal(timeOfUpdate, featureKey, featureVal)
        logInfo('Instrument Features: %s: %s' % (self.__instrumentId, str(currentFeatures)))
