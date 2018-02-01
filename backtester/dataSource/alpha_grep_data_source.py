from datetime import datetime, timedelta
import calendar
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.dataSource.data_source import DataSource
import os.path
from backtester.dataSource.data_source_utils import groupAndSortByTimeUpdates
from pydispatch import dispatcher

DATA_SIGNAL='data_signal'
DATA_SENDER='data_sender'

class AlphaGrepDataSource(DataSource):
    def __init__(self, filePath = 'C:\Users\Shub\Downloads\\bookData'):
        self.filePath = filePath
        self.emitBookData()

    def checkDate(self, lineItem):
        try:
            datetime.strptime(lineItem, '%Y/%m/%d')
            return True
        except ValueError:
            return False


    def checkTimestamp(self, lineItem):
        return True


    # Returns the type of lineItems
    def validateLineItem(self, lineItems):
        if len(lineItems) != 8:
            return False
        if self.checkDate(lineItems[0]) and self.checkTimestamp(lineItems[1]) and (lineItems[2] == 'S' or lineItems[2] == 'F'):
            return True

    def parseBookDataLine(self, lineItems):
        updateType = lineItems[2]
        symbol = lineItems[3]
        bidPrice = float(lineItems[4])
        bidVol = float(lineItems[5])
        askPrice = float(lineItems[6])
        askVol = float(lineItems[7])
        return {'update_type': updateType,
                'symbol': symbol,
                'bid_volume': bidVol,
                'bid_price': bidPrice,
                'ask_price': askPrice,
                'ask_volume': askVol}

    def processLine(self, line):
        lineItems = line.split()
        if(self.validateLineItem(lineItems)):
            return self.parseBookDataLine(lineItems)

    def emitBookData(self):
        with open(self.filePath, "r") as bookData:
            for line in bookData:
                update = self.processLine(line)
                print 'MESSAGE BEING SENT\n'
                dispatcher.send(message=update, signal=DATA_SIGNAL, sender=DATA_SENDER)
