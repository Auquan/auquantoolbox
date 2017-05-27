from instrument_update import InstrumentUpdate


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
    def __init__(self, futureInstrumentId, timeOfUpdate, bookData, expiryTime):
        super.__init__(futureInstrumentId, timeOfUpdate, bookData)
        self.__futureInstrumentId = futureInstrumentId
        self.__expiryTime = expiryTime

    def getExpiryTime(self):
        return self.__expiryTime
