import time
from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import FutureInstrumentUpdate
from datetime import datetime


class LogfileDataSource(DataSource):
    def __init__(self, fileName, liveUpdates=True):
        self.fileName = fileName
        self.file = open(fileName, "r")
        self.file.seek(0, 2)
        self.unfinishedLine = ''
        if not liveUpdates:
            self.processAllInstrumentUpdates()
            self.filterUpdatesByDates()

    '''
    Assume line in processLine is a complete line.
    override this method to return an instrument
    '''
    def processLineIntoInstrumentUpdate(self, line):
        return line

    '''
    Will use child class's processLine
    '''
    # TODO:
    def processLine(self, line):
        lineItems = line.split()
        inst = FutureInstrumentUpdate(futureInstrumentId='AAG',
                                      tradeSymbol=None,
                                      timeOfUpdate=None,
                                      bookData=None,
                                      expiryTime=datetime.strptime("2/1/2018","%m/%d/%Y"),
                                      underlyingInstrumentId='NA')
        return inst


    def emitInstrumentUpdates(self):
        while True:
            readLine = self.file.readline()
            if readLine:
                self.unfinishedLine = self.unfinishedLine + readLine
                if self.unfinishedLine.endswith('\n'):
                    instrumentUpdate = self.processLine(self.unfinishedLine)
                    self.unfinishedLine = ''
                    if instrumentUpdate:
                        yield(instrumentUpdate)
            else:
                time.sleep(0.1)
