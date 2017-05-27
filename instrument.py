import constants
import useful_fn as utils

class Instrument:

    '''
    Instrument: This is a class to represent book data read from log file
    bookData: array of line option data. Dictionary with keys bidVol, bidPrice, askVol, askPrice
    '''
    def __init__(self, time, date, instrumentId, bookData):
        self.time = date + ' ' + time # TODO: standardize this please
        self.instrumentId = instrumentId
        self.bookData = bookData

    def isFuture(self):
        return "-" in self.instrumentId

    def getTypeOfOption(self):
        if self.instrumentId.endsWith("004"):
            return constants.OPTION_TYPE_PUT
        if self.instrumentId.endsWith("003"):
            return constants.OPTION_TYPE_CALL
        print("Error: cant figure out type of option from instrument: " + self.instrumentId)
        return constants.OPTION_TYPE_UNDEFINED

    def getVwap(self):
        return utils.get_vwap(self.bookData['bidVol'],
                              self.bookData['bidPrice'],
                              self.bookData['askPrice'],
                              self.bookData['askVol'])