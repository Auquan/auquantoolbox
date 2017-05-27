from instrument import Instrument


class StockInstrument(Instrument):

    def __init__(self, stockInstrumentId):
    	super.__init__(stockInstrumentId)
        self.__stockInstrumentId = stockInstrumentId

    def getInstrumentType(self):
        return INSTRUMENT_TYPE_STOCK