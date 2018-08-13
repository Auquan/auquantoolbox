from backtester.instruments.instrument import Instrument
from backtester.constants import *


class FutureInstrument(Instrument):

    def __init__(self, futureInstrumentId, bookDataFeatures, expiryTime, underlyingInstrumentId, tsParams):
        super(FutureInstrument, self).__init__(futureInstrumentId, bookDataFeatures, tsParams)
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
