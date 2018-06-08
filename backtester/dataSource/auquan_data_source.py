from datetime import datetime, timedelta
import calendar
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.dataSource.data_source import DataSource
import os.path
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates

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
            'askVolume': askVol}


def get_exp_date(trade_date):
    date = max(week[-4] for week in calendar.monthcalendar(trade_date.year, trade_date.month))
    if date >= trade_date.day:
        exp_date = datetime(year=trade_date.year, month=trade_date.month, day=date)
    else:
        if trade_date.month != 12:
            date = max(week[-4] for week in calendar.monthcalendar(trade_date.year, 1 + trade_date.month))
            exp_date = datetime(year=trade_date.year, month=1 + trade_date.month, day=date)
        else:
            date = max(week[-4] for week in calendar.monthcalendar(1 + trade_date.year, 1))
            exp_date = datetime(year=1 + trade_date.year, month=1, day=date)
    holiday_dates = ['20160706', '20160815', '20160905', '20160913', '20161011', '20161012', '20161031',
                     '20161114', '20170126', '20170224', '20170313', '20170404', '20170414', '20170501', '20170626']
    if datetime.strftime(exp_date, '%Y%m%d') in holiday_dates:
        exp_date = exp_date + timedelta(days=-1)
    return exp_date.replace(hour=15, minute=30)


class InstrumentsFromFile():
    def __init__(self, fileName, instrumentId, expiryTime):
        self.fileName = fileName
        self.instrumentId = instrumentId
        self.expiryTime = expiryTime
        self.currentInstrumentSymbol = None
        self.currentTimeOfUpdate = None
        self.currentBookData = None

    def processLine(self, line):
        lineItems = line.split()
        lineItemType = validateLineItem(lineItems)
        if (lineItemType == TYPE_LINE_BOOK_DATA):
            inst = None
            if self.currentInstrumentSymbol is not None:
                inst = FutureInstrumentUpdate(futureInstrumentId=self.instrumentId,
                                              tradeSymbol=self.currentInstrumentSymbol,
                                              timeOfUpdate=self.currentTimeOfUpdate,
                                              bookData=self.currentBookData,
                                              expiryTime=self.expiryTime,
                                              underlyingInstrumentId='NA')
            self.currentTimeOfUpdate = datetime.strptime(lineItems[0] + ' ' + lineItems[1], "%Y/%m/%d %H:%M:%S:%f")
            self.currentInstrumentSymbol = lineItems[4]
            self.currentBookData = None
            return inst
        elif(lineItemType == TYPE_LINE_BOOK_OPTION):
            parsedOption = parseBookDataOptionLine(lineItems)
            if self.currentBookData is None:
                self.currentBookData = parsedOption

    def processLinesIntoInstruments(self):
        with open(self.fileName, "r") as ins:
            instruments = []
            for line in ins:
                inst = self.processLine(line)
                if inst is not None:
                    instruments.append(inst)
            return instruments


class AuquanDataSource(DataSource):
    def __init__(self, folderName, instrumentIdsByType, startDateStr, endDateStr, liveUpdates=True):
        self.startDate = datetime.strptime(startDateStr, "%Y/%m/%d")
        self.endDate = datetime.strptime(endDateStr, "%Y/%m/%d")
        self.folderName = folderName
        self.instrumentIdsByType = instrumentIdsByType
        self.currentDate = self.startDate
        if not liveUpdates:
            self.processAllInstrumentUpdates()
            self.filterUpdatesByDates([(startDateStr, endDateStr)])

    def getFileName(self, instrumentType, instrumentId, date):
        dateStr = date.strftime("%Y%m%d")
        return '%s/%s/%s/%s_%s.txt' % (self.folderName, instrumentType, instrumentId, instrumentId, dateStr)

    def emitInstrumentUpdates(self):
        while (self.currentDate <= self.endDate):
            allInstrumentUpdates = []
            for instrumentType in self.instrumentIdsByType:
                instrumentIds = self.instrumentIdsByType[instrumentType]
                for instrumentId in instrumentIds:
                    fileName = self.getFileName(instrumentType, instrumentId, self.currentDate)
                    if not os.path.isfile(fileName):
                        continue
                    expiryTime = get_exp_date(self.currentDate)
                    fileHandler = InstrumentsFromFile(fileName=fileName, instrumentId=instrumentId, expiryTime=expiryTime)
                    instrumentUpdates = fileHandler.processLinesIntoInstruments()
                    allInstrumentUpdates = allInstrumentUpdates + instrumentUpdates
            timeUpdates, groupedInstrumentUpdates = groupAndSortByTimeUpdates(allInstrumentUpdates)
            for timeOfUpdate, instrumentUpdates in groupedInstrumentUpdates:
                yield([timeOfUpdate, instrumentUpdates])
            self.currentDate = self.currentDate + timedelta(days=1)


if __name__ == "__main__":
    a = datetime.strptime('2017/06/30', "%Y/%m/%d")
    print(get_exp_date(a))
