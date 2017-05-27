from data_source import DataSource
import pandas as pd
from datetime import datetime

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


class NiftyDataSource(DataSource):
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, "r")
        self.file.seek(0, 2)
        self.unfinishedLine = ''
        self.currentTime = ''
        self.currentDate = ''
        self.currentInstrumentId = None
        self.currentBookData = []

    def processLine(self, line):
        accumulatedInstruments = []
        lineItems = line.split()
        lineItemType = validateLineItem(lineItems)

        if (lineItemType == TYPE_LINE_BOOK_DATA):
            if self.currentInstrumentId is not None:
                inst = instrument.Instrument(time=self.currentTime,
                                             date=self.currentDate,
                                             instrumentId=self.currentInstrumentId,
                                             bookData=pd.DataFrame(self.currentBookData, columns=['bidVol', 'bidPrice', 'askPrice', 'askVol']))
                self.currentDate = lineItems[0]
                self.currentTime = lineItems[1]
                self.currentInstrumentId = lineItems[4]
                self.currentBookData = []
                return inst
            elif(lineItemType == TYPE_LINE_BOOK_OPTION):
                parsedOption = parseBookDataOptionLine(lineItems)
                self.currentBookData.append(parsedOption)

    def emitInstrumentUpdate(self):
        while True:
            readLine = self.file.readline()
            if readLine:
                self.unfinishedLine = self.unfinishedLine + readLine
                if self.unfinishedLine.endswith('\n'):
                    self.unfinishedLine = ''
                    instrumentUpdate = self.processLine(self.unfinishedLine)
                    if instrumentUpdate:
                        yield(instrumentUpdate)
