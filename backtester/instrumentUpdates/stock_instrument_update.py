from instrument_update import InstrumentUpdate


class StockInstrumentUpdate(InstrumentUpdate):
    '''
    stockInstrumentId: symbol for stock
    timeOfUpdate: datetime object for time of update
    bookData: dictionary. keys which we support right now:
             bidPrice
             bidVolume
             askPrice
             askVolume
             volume
             open
             close
             high
             low
    '''
    def __init__(self, stockInstrumentId, timeOfUpdate, bookData):
        super.__init__(stockInstrumentId, timeOfUpdate, bookData)
        self.__stockInstrumentId = stockInstrumentId

    def getStockInstrumentId(self):
        return __stockInstrumentId

    def getTypeOfInstrument(self):
        return INSTRUMENT_TYPE_STOCK
