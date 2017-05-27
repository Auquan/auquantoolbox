from instrument import Instrument


class OptionInstrument(Instrument):

    def __init__(self, optionInstrumentId, strikePrice, expiryTime):
        self.__optionInstrumentId = optionInstrumentId
        self.__strikePrice = strikePrice
        self.__expiryTime = expiryTime

    '''
    Returns datettime object for expiry of option
    '''
    def getExpiryTime(self):
        return self.__expiryTime

    def getStrikePrice(self):
        return self.__strikePrice
