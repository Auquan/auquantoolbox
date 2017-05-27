from instrument import Instrument


class FutureInstrument(Instrument):

    def __init__(self, futureInstrumentId, expiryTime, underlyingInstrumentId):
    	super.__init__(futureInstrumentId)
        self.__futureInstrumentId = futureInstrumentId
        self.__expiryTime = expiryTime
        self.__underlyingInstrumentId = underlyingInstrumentId

    def getInstrumentType(self):
        return INSTRUMENT_TYPE_FUTURE
    '''
    Returns datettime object for expiry of option
    '''
    def getExpiryTime(self):
        return self.__expiryTime

    def getUnderlyingInstrumentId(self):
    	return self.__underlyingInstrumentId
