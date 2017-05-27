class InstrumentManager:
    def __init__(self):
        self.__instrumentsDict = {}
        # TODO: create a different place to hold different types of instruments

    def getInstrument(self, instrumentId):
        return self.instrumentsDict[instrumentId]

    def createInstrumentFromUpdate(self, instrumentUpdate):
        type = instrumentUpdate.getTypeOfInstrument()
        instrument = None
        if type == INSTRUMENT_TYPE_STOCK:
            stockInstrumentId = instrumentUpdate.getStockInstrumentId()
            instrument = StockInstrument(stockInstrumentId=stockInstrumentId)
        elif type == INSTRUMENT_TYPE_FUTURE:
            futureInstrumentId = instrumentUpdate.getFutureInstrumentId()
            expiryTime = instrumentUpdate.getExpiryTime()
            underlyingInstrumentId = instrumentUpdate.getUnderlyingInstrumentId()
            instrument = FutureInstrument(futureInstrumentId=futureInstrumentId, 
                                          expiryTime=expiryTime, 
                                          underlyingInstrumentId=underlyingInstrumentId)
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
                                          underlyingInstrumentId=underlyingInstrumentId)
        return instrument

    def addInstrument(self, instrument):
        instrumentId = instrument.getInstrumentId()
        self.__instrumentsDict[instrumentId] = instrument

    def updateFeatures(self, timeOfUpdate):
        for instrumentId in self.instrumentsDict:
            instrument = self.instrumentsDict[instrumentId]
            instrument.updateFeatures(timeOfUpdate)


