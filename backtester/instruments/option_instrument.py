from instrument import Instrument


class OptionInstrument(Instrument):

    def __init__(self, optionInstrumentId, strikePrice, optionType, expiryTime, underlyingInstrumentId):
        super.__init__(optionInstrumentId)
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
