from backtester.constants import *
from lookback_data import LookbackData
from marketFeatures.market_feature import MarketFeature


class InstrumentManager:
    def __init__(self):
        self.__instrumentsDict = {}
        # TODO: create a different place to hold different types of instruments
        self.__lookbackMarketFeatures = LookbackData()

    def getInstrument(self, instrumentId):
        return self.instrumentsDict[instrumentId]

    def getLookbackMarketFeatures(self):
        return self.__lookbackMarketFeatures

    def createInstrumentFromUpdate(self, instrumentUpdate, tsParams):
        type = instrumentUpdate.getTypeOfInstrument()
        instrument = None
        if type == INSTRUMENT_TYPE_STOCK:
            stockInstrumentId = instrumentUpdate.getStockInstrumentId()
            instrument = StockInstrument(stockInstrumentId=stockInstrumentId,
                                         tsParams=tsParams)
        elif type == INSTRUMENT_TYPE_FUTURE:
            futureInstrumentId = instrumentUpdate.getFutureInstrumentId()
            expiryTime = instrumentUpdate.getExpiryTime()
            underlyingInstrumentId = instrumentUpdate.getUnderlyingInstrumentId()
            instrument = FutureInstrument(futureInstrumentId=futureInstrumentId,
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
        for instrumentId in self.instrumentsDict:
            instrument = self.instrumentsDict[instrumentId]
            instrument.updateFeatures(timeOfUpdate)

        currentMarketFeatures = {}
        featureConfigs = self.tsParams.getMarketFeatureConfigs()
        for featureConfig in featureConfigs:
            featureId = featureConfig.getFeatureId()
            featureParams = featureConfig.getFeatureParams()
            featureVal = MarketFeature.computeForFeature(instrumentFeatureId=featureId,
                                                         featureParams=featureParams,
                                                         currentMarketFeatures=currentMarketFeatures,
                                                         instrumentManager=self)
            currentMarketFeatures[featureConfig.getFeatureKey()] = featureVal
        currentMarketFeatures['prediction'] = self.tsParams.getPrediction(timeOfUpdate, currentMarketFeatures, self)
        self.__lookbackFeatures.addData(currentMarketFeatures)
