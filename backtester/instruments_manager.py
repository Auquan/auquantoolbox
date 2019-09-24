from backtester.constants import *
from backtester.lookback_data import LookbackData
from backtester.features.feature_config import FeatureConfig
from backtester.instruments import *
from backtester.logger import *
from itertools import chain
from backtester.instruments_lookback_data import InstrumentsLookbackData
import time


def getCompulsoryMarketFeatureConfigs(tsParams):
    profitlossConfigDict = {'featureKey': 'pnl',
                            'featureId': 'pnl',
                            'params': {'instrument_pnl_feature': 'pnl'}}
    capitalConfigDict = {'featureKey': 'capital',
                         'featureId': 'capital',
                         'params': {'initial_capital': tsParams.getStartingCapital(),
                                    'pnl': 'pnl'}}
    portfoliovalueConfigDict = {'featureKey': 'portfolio_value',
                                'featureId': 'portfolio_value',
                                'params': {'initial_capital': tsParams.getStartingCapital(),
                                           'pnl': 'pnl'}}
    varianceConfigDict = {'featureKey': 'variance',
                          'featureId': 'variance',
                          'params': {'pnlKey': 'pnl'}}
    maxCapitalUsageConfigDict = {'featureKey': 'capitalUsage',
                                 'featureId': 'maxCapitalUsage',
                                 'params': {'initial_capital': tsParams.getStartingCapital(),
                                            'capitalKey': 'capital'}}
    maxDrawdownConfigDict = {'featureKey': 'maxDrawdown',
                             'featureId': 'maxDrawdown',
                             'params': {'portfolioValueKey': 'portfolio_value'}}
    totalProfitConfigDict = {'featureKey': 'total_profit',
                             'featureId': 'total_profit',
                             'params': {'pnlKey': 'pnl'}}
    totalLossConfigDict = {'featureKey': 'total_loss',
                           'featureId': 'total_loss',
                           'params': {'pnlKey': 'pnl'}}
    countProfitConfigDict = {'featureKey': 'count_profit',
                             'featureId': 'count_profit',
                             'params': {'pnlKey': 'pnl'}}
    countLossConfigDict = {'featureKey': 'count_loss',
                           'featureId': 'count_loss',
                           'params': {'pnlKey': 'pnl'}}
    compulsoryConfigDicts = [profitlossConfigDict, capitalConfigDict, portfoliovalueConfigDict,
                             varianceConfigDict, maxCapitalUsageConfigDict, maxDrawdownConfigDict,
                             totalProfitConfigDict, totalLossConfigDict, countProfitConfigDict, countLossConfigDict]
    compulsoryMarketFeatureConfigs = list(map(lambda x: FeatureConfig(x), compulsoryConfigDicts))
    return compulsoryMarketFeatureConfigs


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
    totalProfitConfigDict = {'featureKey': 'total_profit',
                             'featureId': 'total_profit',
                             'params': {'pnlKey': 'pnl'}}
    totalLossConfigDict = {'featureKey': 'total_loss',
                           'featureId': 'total_loss',
                           'params': {'pnlKey': 'pnl'}}
    countProfitConfigDict = {'featureKey': 'count_profit',
                             'featureId': 'count_profit',
                             'params': {'pnlKey': 'pnl'}}
    countLossConfigDict = {'featureKey': 'count_loss',
                           'featureId': 'count_loss',
                           'params': {'pnlKey': 'pnl'}}
    compulsoryConfigDicts = [positionConfigDict, feesConfigDict[instrumentType], profitlossConfigDict, capitalConfigDict,
                             totalProfitConfigDict, totalLossConfigDict, countProfitConfigDict, countLossConfigDict]
    compulsoryInstrumentFeatureConfigs = list(map(lambda x: FeatureConfig(x), compulsoryConfigDicts))
    return compulsoryInstrumentFeatureConfigs


class InstrumentManager:
    def __init__(self, tsParams, bookDataFeatures, instrumentIds, frequencyGetter, initializer=None):
        self.tsParams = tsParams
        self.__instrumentsDict = {}
        # TODO: create a different place to hold different types of instruments
        featureConfigs = tsParams.getMarketFeatureConfigs()
        self.__compulsoryFeatureConfigs = getCompulsoryMarketFeatureConfigs(tsParams)
        columns = map(lambda x: x.getFeatureKey(), featureConfigs)
        compulsoryColumns = map(lambda x: x.getFeatureKey(), self.__compulsoryFeatureConfigs)
        marketFeatureKeys = list(chain(columns, compulsoryColumns))
        self.__lookbackMarketFeatures = LookbackData(tsParams.getLookbackSize(), marketFeatureKeys, initializer)

        self.__bookDataFeatures = bookDataFeatures or {}
        self.__compulsoryInstrumentFeatureConfigs = getCompulsoryInstrumentFeatureConfigs(tsParams, INSTRUMENT_TYPE_STOCK)
        instrumentFeatureConfigs = tsParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)
        compulsoryInstrumentFeatureKeys = map(lambda x: x.getFeatureKey(), self.__compulsoryInstrumentFeatureConfigs)
        instrumentFeatureKeys = map(lambda x: x.getFeatureKey(), instrumentFeatureConfigs)
        featureKeys = list(chain(self.__bookDataFeatures, instrumentFeatureKeys, compulsoryInstrumentFeatureKeys))
        self.__lookbackInstrumentFeatures = InstrumentsLookbackData(size=tsParams.getLookbackSize(),
                                                                    features=featureKeys,
                                                                    instrumentIds=instrumentIds,
                                                                    frequencyGetter=frequencyGetter,
                                                                    initializer=initializer)

        self.__totalIter = 0
        self.__perfDict = {}
        self.__marketPerfDict = {}
        for featureKey in marketFeatureKeys:
            self.__marketPerfDict[featureKey] = 0
        for featureKey in featureKeys:
            self.__perfDict[featureKey] = 0

    def getTsParams(self):
        return self.tsParams

    def getInstrument(self, instrumentId):
        if instrumentId not in self.__instrumentsDict:
            return None
        return self.__instrumentsDict[instrumentId]

    def getAllInstrumentIds(self):
        return self.__lookbackInstrumentFeatures._InstrumentsLookbackData__instrumentIds

    def getAllInstrumentsByInstrumentId(self):
        return self.__instrumentsDict

    def getLookbackMarketFeatures(self):
        return self.__lookbackMarketFeatures

    def getLookbackInstrumentFeatures(self):
        return self.__lookbackInstrumentFeatures

    def getLookbackInstrumentFeaturesForFeature(self, featureKey):
        return self.__lookbackInstrumentFeatures.getFeatureDf(featureKey)

    def getDataDf(self):
        return self.__lookbackMarketFeatures.getData()

    def createInstrumentFromUpdate(self, instrumentUpdate, tsParams):
        type = instrumentUpdate.getTypeOfInstrument()
        bookDataFeatures = instrumentUpdate.getBookDataFeatures()
        instrument = None
        if type == INSTRUMENT_TYPE_STOCK:
            stockInstrumentId = instrumentUpdate.getStockInstrumentId()
            instrument = StockInstrument(stockInstrumentId=stockInstrumentId,
                                         bookDataFeatures=bookDataFeatures,
                                         tsParams=tsParams)
        elif type == INSTRUMENT_TYPE_FUTURE:
            futureInstrumentId = instrumentUpdate.getFutureInstrumentId()
            expiryTime = instrumentUpdate.getExpiryTime()
            underlyingInstrumentId = instrumentUpdate.getUnderlyingInstrumentId()
            instrument = FutureInstrument(futureInstrumentId=futureInstrumentId,
                                          bookDataFeatures=bookDataFeatures,
                                          expiryTime=expiryTime,
                                          underlyingInstrumentId=underlyingInstrumentId,
                                          tsParams=tsParams)
        elif type == INSTRUMENT_TYPE_OPTION:
            optionInstrumentId = instrumentUpdate.getOptionInstrumentId()
            strikePrice = instrumentUpdate.getStrikePrice()
            optionType = instrumentUpdate.getOptionType()
            expiryTime = instrumentUpdate.getExpiryTime()
            underlyingInstrumentId = instrumentUpdate.getUnderlyingInstrumentId()
            instrument = OptionInstrument(optionInstrumentId=optionInstrumentId,
                                          bookDataFeatures=bookDataFeatures,
                                          strikePrice=strikePrice,
                                          optionType=optionType,
                                          expiryTime=expiryTime,
                                          underlyingInstrumentId=underlyingInstrumentId,
                                          tsParams=tsParams)
        return instrument

    def addInstrument(self, instrument):
        instrumentId = instrument.getInstrumentId()
        self.__instrumentsDict[instrumentId] = instrument

    def updateInstrumentFeatures(self, timeOfUpdate):
        self.__totalIter = self.__totalIter + 1

        # populate current book data
        currentBookDataByFeature = {}
        for featureKey in self.__bookDataFeatures:
            currentBookDataByFeature[featureKey] = {}
        for instrument in self.__instrumentsDict.values():
            instrumentId = instrument.getInstrumentId()
            currentInstrumentBookData = instrument.getCurrentBookData()
            for featureKey in self.__bookDataFeatures:
                currentBookDataByFeature[featureKey][instrumentId] = currentInstrumentBookData[featureKey]

        for featureKey in self.__bookDataFeatures:
            start = time.time()
            self.__lookbackInstrumentFeatures.addFeatureValueForAllInstruments(timeOfUpdate, featureKey, currentBookDataByFeature[featureKey])
            end = time.time()
            diffms = (end - start) * 1000
            self.__perfDict[featureKey] = self.__perfDict[featureKey] + diffms
            logPerf('Avg time for feature: %s : %.2f' % (featureKey, self.__perfDict[featureKey] / self.__totalIter))
        featureConfigs = self.tsParams.getFeatureConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)  # TODO:
        featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        for featureConfig in self.__compulsoryInstrumentFeatureConfigs:  # TODO: Find a better way to handle compulsory dicts
            featureKey = featureConfig.getFeatureKey()
            if featureKey in featureConfigKeys:
                i = featureConfigKeys.index(featureKey)
                customFeatureConfig = featureConfigs.pop(i)
                featureConfigKeys.pop(i)
                featureConfigs.append(customFeatureConfig)
            else:
                featureConfigs.append(featureConfig)

        featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        for featureConfig in featureConfigs:
            start = time.time()
            featureKey = featureConfig.getFeatureKey()
            featureId = featureConfig.getFeatureId()
            featureParams = featureConfig.getFeatureParams()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
            featureVal = featureCls.computeForInstrument(updateNum=self.__totalIter,
                                                         time=timeOfUpdate,
                                                         featureParams=featureParams,
                                                         featureKey=featureKey,
                                                         instrumentManager=self)
            self.__lookbackInstrumentFeatures.addFeatureValueForAllInstruments(timeOfUpdate, featureKey, featureVal)
            end = time.time()
            diffms = (end - start) * 1000
            self.__perfDict[featureKey] = self.__perfDict[featureKey] + diffms
            logPerf('Avg time for feature: %s : %.2f' % (featureKey, self.__perfDict[featureKey] / self.__totalIter))

    def updateFeatures(self, timeOfUpdate):
        self.updateInstrumentFeatures(timeOfUpdate)

        currentMarketFeatures = {}
        self.__lookbackMarketFeatures.addData(timeOfUpdate, currentMarketFeatures)
        featureConfigs = self.tsParams.getMarketFeatureConfigs()
        featureConfigKeys = [featureConfig.getFeatureKey() for featureConfig in featureConfigs]
        for featureConfig in self.__compulsoryFeatureConfigs:  # TODO: Find a better way to handle compulsory dicts
            featureKey = featureConfig.getFeatureKey()
            if featureKey in featureConfigKeys:
                i = featureConfigKeys.index(featureKey)
                customFeatureConfig = featureConfigs.pop(i)
                featureConfigKeys.pop(i)
                featureConfigs.append(customFeatureConfig)
            else:
                featureConfigs.append(featureConfig)
        for featureConfig in featureConfigs:
            start = time.time()
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
            featureVal = featureCls.computeForMarket(updateNum=self.__totalIter,
                                                     time=timeOfUpdate,
                                                     featureParams=featureParams,
                                                     featureKey=featureKey,
                                                     currentMarketFeatures=currentMarketFeatures,
                                                     instrumentManager=self)
            currentMarketFeatures[featureKey] = featureVal
            self.__lookbackMarketFeatures.addFeatureVal(timeOfUpdate, featureKey, featureVal)
            end = time.time()
            diffms = (end - start) * 1000
            self.__marketPerfDict[featureKey] = self.__marketPerfDict[featureKey] + diffms
            logPerf('Avg time for feature: %s : %.2f' % (featureKey, self.__marketPerfDict[featureKey] / self.__totalIter))

        logInfo('Market Features: %s' % str(currentMarketFeatures))
