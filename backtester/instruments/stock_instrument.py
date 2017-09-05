from backtester.instruments.instrument import Instrument
from backtester.constants import *


class StockInstrument(Instrument):

    def __init__(self, stockInstrumentId, bookDataFeatures, tsParams):
        super(StockInstrument, self).__init__(stockInstrumentId, bookDataFeatures, tsParams)
        self.__stockInstrumentId = stockInstrumentId

    def getInstrumentType(self):
        return INSTRUMENT_TYPE_STOCK
