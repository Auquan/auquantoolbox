from backtester.instrumentUpdates.instrument_update import InstrumentUpdate
from backtester.constants import *


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
    def __init__(self, optionInstrumentId, tradeSymbol, timeOfUpdate, bookData, strikePrice, optionType, expiryTime, underlyingInstrumentId):
        super(OptionInstrumentUpdate, self).__init__(optionInstrumentId, tradeSymbol, timeOfUpdate, bookData)
        self.__optionInstrumentId = optionInstrumentId
        self.__expiryTime = expiryTime
        self.__strikePrice = strikePrice
        self.__optionType = optionType
        self.__underlyingInstrumentId = underlyingInstrumentId

    def getOptionInstrumentId():
        return self.__optionInstrumentId

    def getTypeOfInstrument(self):
        return INSTRUMENT_TYPE_OPTION

    def getExpiryTime(self):
        return self.__expiryTime

    def getStrikePrice(self):
        return self.__strikePrice

    def getOptionType(self):
        return self.__optionType

    def getUnderlyingInstrumentId(self):
        return self.__underlyingInstrumentId
