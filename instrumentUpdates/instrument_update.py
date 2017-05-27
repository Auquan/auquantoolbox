'''
A base class to represent an update to instrument.
'''


class InstrumentUpdate:
    '''
    instrumentId: unique id to represent the instrument
    timeOfUpdate: datetime object for time of update
    expiryTime: datettime object for expiry of option
    bookData: dictionary of things specific to the instrument.
    '''
    def __init__(self, instrumentId, timeOfUpdate, bookData):
        self.__instrumentId = instrumentId
        self.__timeOfUpdate = timeOfUpdate
        self.__bookData = bookData

    '''
    Returns a string to represent a unique identifier for the instrument
    '''
    def getInstrumentId(self):
        return self.__instrumentId

    def getBookData(self):
        return self.__bookData

    def getTimeOfUpdate(self):
        return self.__timeOfUpdate
