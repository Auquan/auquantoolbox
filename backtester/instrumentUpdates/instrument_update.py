from backtester.constants import *
'''
A base class to represent an update to instrument.
'''


class InstrumentUpdate(object):
    '''
    instrumentId: unique id to represent the instrument
    timeOfUpdate: datetime object for time of update
    expiryTime: datettime object for expiry of option
    bookData: dictionary of things specific to the instrument.
    '''
    def __init__(self, instrumentId, tradeSymbol, timeOfUpdate, bookData):
        self.__instrumentId = instrumentId
        self.__tradeSymbol = tradeSymbol
        self.__timeOfUpdate = timeOfUpdate
        self.__bookData = bookData

    '''
    Returns a string to represent a unique identifier for the instrument
    '''
    def getInstrumentId(self):
        return self.__instrumentId

    def getTradeSymbol(self):
        return self.__tradeSymbol

    def getBookData(self):
        return self.__bookData

    def getBookDataFeatures(self):
        return self.__bookData.keys()

    def getTimeOfUpdate(self):
        return self.__timeOfUpdate

    def getTypeOfInstrument(self):
        raise "Unimplemented error"
        return INSTRUMENT_TYPE_UNDEFINED
