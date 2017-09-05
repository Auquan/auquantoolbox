from backtester.constants import *
from backtester.lookback_data import LookbackData
from backtester.features.feature_config import FeatureConfig
from backtester.instruments import *
from backtester.logger import *


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
    compulsoryConfigDicts = [profitlossConfigDict, capitalConfigDict, portfoliovalueConfigDict]
    compulsoryMarketFeatureConfigs = map(lambda x: FeatureConfig(x), compulsoryConfigDicts)
    return compulsoryMarketFeatureConfigs


class InstrumentManager:
    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.__instrumentsDict = {}
        # TODO: create a different place to hold different types of instruments
        featureConfigs = tsParams.getMarketFeatureConfigs()
        self.__compulsoryFeatureConfigs = getCompulsoryMarketFeatureConfigs(tsParams)
        columns = map(lambda x: x.getFeatureKey(), featureConfigs)
        compulsoryColumns = map(lambda x: x.getFeatureKey(), self.__compulsoryFeatureConfigs)
        self.__lookbackMarketFeatures = LookbackData(tsParams.getLookbackSize(), columns + compulsoryColumns + ['prediction'])

    def getInstrument(self, instrumentId):
        if instrumentId not in self.__instrumentsDict:
            return None
        return self.__instrumentsDict[instrumentId]

    def getAllInstrumentsByInstrumentId(self):
        return self.__instrumentsDict

    def getLookbackMarketFeatures(self):
        return self.__lookbackMarketFeatures

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

    def updateFeatures(self, timeOfUpdate):
        for instrumentId in self.__instrumentsDict:
            instrument = self.__instrumentsDict[instrumentId]
            instrument.updateFeatures(timeOfUpdate, self)

        currentMarketFeatures = {}
        featureConfigs = self.tsParams.getMarketFeatureConfigs() + self.__compulsoryFeatureConfigs
        for featureConfig in featureConfigs:
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = FeatureConfig.getClassForFeatureId(featureId)
            featureVal = featureCls.computeForMarket(featureParams=featureParams,
                                                     featureKey=featureKey,
                                                     currentMarketFeatures=currentMarketFeatures,
                                                     instrumentManager=self)
            currentMarketFeatures[featureKey] = featureVal
        currentMarketFeatures['prediction'] = self.tsParams.getPrediction(timeOfUpdate, currentMarketFeatures, self)

        logInfo('Market Features: %s' % str(currentMarketFeatures))
        self.__lookbackMarketFeatures.addData(timeOfUpdate, currentMarketFeatures)
