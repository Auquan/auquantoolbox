from instrument_update import InstrumentUpdate


class OptionInstrumentUpdate(InstrumentUpdate):
    '''
    optionInstrumentId: symbol for option id
    timeOfUpdate: datetime object for time of update
    expiryTime: datettime object for expiry of option
    bookData: dictionary. keys which we support right now:
             bidPrice
             bidVolume
             askPrice
             askVolume
             volume
             openInterest
    '''
    def __init__(self, optionInstrumentId, timeOfUpdate, bookData, expiryTime):
        super.__init__(optionInstrumentId, timeOfUpdate, bookData)
        self.__optionInstrumentId = optionInstrumentId
        self.__expiryTime = expiryTime

    def getExpiryTime(self):
        return self.__expiryTime
