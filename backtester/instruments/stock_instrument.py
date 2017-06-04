from instrument import Instrument
from backtester.constants import *


class StockInstrument(Instrument):

    def __init__(self, stockInstrumentId, tsParams):
        super(StockInstrument, self).__init__(stockInstrumentId, tsParams)
        self.__stockInstrumentId = stockInstrumentId

    def getInstrumentType(self):
        return INSTRUMENT_TYPE_STOCK
