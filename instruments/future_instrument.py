from instrument import Instrument


class FutureInstrument(Instrument):

    def __init__(self, futureInstrumentId, expiryTime):
        self.__futureInstrumentId = futureInstrumentId
        self.__expiryTime = expiryTime

    '''
    Returns datettime object for expiry of option
    '''
    def getExpiryTime(self):
        return self.__expiryTime
