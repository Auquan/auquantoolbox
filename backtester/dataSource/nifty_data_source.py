from datetime import datetime
from instrumentUpdates import *
from constants import *
from logfile_data_source import LogfileDataSource

TYPE_LINE_UNDEFINED = 0
TYPE_LINE_BOOK_DATA = 1
TYPE_LINE_GREEK = 2  # not used anymore
TYPE_LINE_BOOK_OPTION = 3


def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%Y/%m/%d')
        return True
    except ValueError:
        return False


def checkTimestamp(lineItem):
    return True


# Returns the type of lineItems
def validateLineItem(lineItems):
    if len(lineItems) < 4:
        return TYPE_LINE_UNDEFINED
    if checkDate(lineItems[0]) and checkTimestamp(lineItems[1]) and lineItems[2] == "Book":
        return TYPE_LINE_BOOK_DATA
    if checkDate(lineItems[0]) and checkTimestamp(lineItems[1]) and lineItems[2] == "Greek:":
        return TYPE_LINE_GREEK
    if len(lineItems) == 7 and lineItems[3] == '|':
        return TYPE_LINE_BOOK_OPTION
    return TYPE_LINE_UNDEFINED


def parseBookDataOptionLine(lineItems):
    if (len(lineItems) < 7):
        return None
    bidVol = float(lineItems[1])
    bidPrice = float(lineItems[2])
    askPrice = float(lineItems[4])
    askVol = float(lineItems[5])
    return {'bidVolume': bidVol,
            'bidPrice': bidPrice,
            'askPrice': askPrice,
            'askVol': askVol}


class NiftyDataSource(LogfileDataSource):
    def __init__(self, fileName, futureInstrumentId, expiryTimeStr):
        super(self.__class__, self).__init__(fileName)
        self.futureInstrumentId = futureInstrumentId
        self.expiryTime = datetime.strptime(expiryTimeStr, "%m/%d/%Y %H:%M:%S")
        self.currentInstrumentId = None
        self.currentTimeOfUpdate = None
        self.currentBookData = None

    def processLine(self, line):
        lineItems = line.split()
        lineItemType = validateLineItem(lineItems)

        if (lineItemType == TYPE_LINE_BOOK_DATA):
            if self.currentInstrumentId is not None:
                inst = None
                if self.currentInstrumentId == self.futureInstrumentId:
                    inst = FutureInstrumentUpdate(futureInstrumentId=self.currentInstrumentId,
                                                  timeOfUpdate=self.currentTimeOfUpdate,
                                                  bookData=self.currentBookData,
                                                  expiryTime=self.expiryTime,
                                                  underlyingInstrumentId='NA')
                else:
                    strikePrice = float(self.currentInstrumentId[-8:-3])
                    optionType = OPTION_TYPE_CALL if self.currentInstrumentId[-3:] == "003" else OPTION_TYPE_PUT
                    inst = OptionInstrumentUpdate(optionInstrumentId=self.currentInstrumentId,
                                                  timeOfUpdate=self.currentTimeOfUpdate,
                                                  bookData=self.currentBookData,
                                                  strikePrice=strikePrice,
                                                  optionType=optionType,
                                                  expiryTime=self.expiryTime,
                                                  underlyingInstrumentId=self.futureInstrumentId)
                self.currentTimeOfUpdate = datetime.strptime(lineItems[0] + ' ' + lineItems[1], "%Y/%m/%d %H:%M:%S:%f")
                self.currentInstrumentId = lineItems[4]
                self.currentBookData = None
                return inst
            elif(lineItemType == TYPE_LINE_BOOK_OPTION):
                parsedOption = parseBookDataOptionLine(lineItems)
                if self.currentBookData is None:
                    self.currentBookData = parsedOption
