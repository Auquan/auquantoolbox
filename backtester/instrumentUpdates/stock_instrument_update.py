from backtester.instrumentUpdates.instrument_update import InstrumentUpdate
from backtester.constants import *


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
    def __init__(self, stockInstrumentId, tradeSymbol, timeOfUpdate, bookData):
        super(StockInstrumentUpdate, self).__init__(stockInstrumentId, tradeSymbol, timeOfUpdate, bookData)
        self.__stockInstrumentId = stockInstrumentId

    def getStockInstrumentId(self):
        return self.__stockInstrumentId

    def getTypeOfInstrument(self):
        return INSTRUMENT_TYPE_STOCK
