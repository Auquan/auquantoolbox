from instrument import Instrument


class StockInstrument(Instrument):

    def __init__(self, stockInstrumentId, expiryTime):
        self.__stockInstrumentId = stockInstrumentId
