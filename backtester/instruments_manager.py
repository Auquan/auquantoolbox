from backtester.constants import *
from backtester.lookback_data import LookbackData
from backtester.marketFeatures.market_feature_config import MarketFeatureConfig
from backtester.instruments import *
from backtester.logger import *


class InstrumentManager:
    def __init__(self, tsParams):
        self.tsParams = tsParams
        self.__instrumentsDict = {}
        # TODO: create a different place to hold different types of instruments
        featureConfigs = tsParams.getMarketFeatureConfigs()
        columns = map(lambda x: x.getFeatureKey(), featureConfigs)
        columns.append('prediction')
        self.__lookbackMarketFeatures = LookbackData(tsParams.getLookbackSize(), columns)

    def getInstrument(self, instrumentId):
        if instrumentId not in self.__instrumentsDict:
            return None
        return self.__instrumentsDict[instrumentId]

    def getAllInstrumentsByInstrumentId(self):
        return self.__instrumentsDict

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
        for instrumentId in self.__instrumentsDict:
            instrument = self.__instrumentsDict[instrumentId]
            instrument.updateFeatures(timeOfUpdate)

        currentMarketFeatures = {}
        featureConfigs = self.tsParams.getMarketFeatureConfigs()
        for featureConfig in featureConfigs:
            featureId = featureConfig.getFeatureId()
            featureKey = featureConfig.getFeatureKey()
            featureParams = featureConfig.getFeatureParams()
            featureCls = MarketFeatureConfig.getClassForMarketFeatureId(featureId)
            featureVal = featureCls.compute(featureParams=featureParams,
                                            featureKey=featureKey,
                                            currentMarketFeatures=currentMarketFeatures,
                                            instrumentManager=self)
            currentMarketFeatures[featureKey] = featureVal
        currentMarketFeatures['prediction'] = self.tsParams.getPrediction(timeOfUpdate, currentMarketFeatures, self)
        logInfo('Market Features: %s' % str(currentMarketFeatures))
        self.__lookbackMarketFeatures.addData(timeOfUpdate, currentMarketFeatures)
