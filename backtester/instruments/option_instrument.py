from backtester.instruments.instrument import Instrument
from backtester.constants import *


class OptionInstrument(Instrument):

    def __init__(self, optionInstrumentId, bookDataFeatures, strikePrice, optionType, expiryTime, underlyingInstrumentId, tsParams):
        super(OptionInstrument, self).__init__(optionInstrumentId, bookDataFeatures, tsParams)
        self.__optionInstrumentId = optionInstrumentId
        self.__strikePrice = strikePrice
        self.__optionType = optionType
        self.__expiryTime = expiryTime
        self.__underlyingInstrumentId = underlyingInstrumentId

    def getInstrumentType(self):
        return INSTRUMENT_TYPE_OPTION

    def getOptionInstrumentId():
        return self.__optionInstrumentId

    '''
    Returns datettime object for expiry of option
    '''
    def getExpiryTime(self):
        return self.__expiryTime

    def getStrikePrice(self):
        return self.__strikePrice

    def getOptionType(self):
        return self.__optionType

    def getUnderlyingInstrumentId(self):
        return self.__underlyingInstrumentId
