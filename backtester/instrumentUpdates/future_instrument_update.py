from backtester.instrumentUpdates.instrument_update import InstrumentUpdate
from backtester.constants import *


class FutureInstrumentUpdate(InstrumentUpdate):
    '''
    futureInstrumentId: symbol for future id
    timeOfUpdate: datetime object for time of update
    expiryTime: datettime object for expiry of future
    bookData: dictionary. keys which we support right now:
             bidPrice
             bidVolume
             askPrice
             askVolume
             volume
             openInterest
             open
             close
             high
             low
    '''
    def __init__(self, futureInstrumentId, tradeSymbol, timeOfUpdate, bookData, expiryTime, underlyingInstrumentId):
        super(FutureInstrumentUpdate, self).__init__(futureInstrumentId, tradeSymbol, timeOfUpdate, bookData)
        self.__futureInstrumentId = futureInstrumentId
        self.__expiryTime = expiryTime
        self.__underlyingInstrumentId = underlyingInstrumentId

    def getFutureInstrumentId(self):
        return self.__futureInstrumentId

    def getTypeOfInstrument(self):
        return INSTRUMENT_TYPE_FUTURE

    def getExpiryTime(self):
        return self.__expiryTime

    def getUnderlyingInstrumentId(self):
        return self.__underlyingInstrumentId
