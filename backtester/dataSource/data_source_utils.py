from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
import os
import os.path
import requests
import re
from time import mktime as mktime
from itertools import groupby


def getCookieForYahoo(instrumentId):
    """Returns a tuple pair of cookie and crumb used in the request"""
    url = 'https://finance.yahoo.com/quote/%s/history' % (instrumentId)
    req = requests.get(url)
    txt = req.content
    cookie = req.cookies['B']
    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

    for line in txt.splitlines():
        m = pattern.match(line.decode("utf-8"))
        if m is not None:
            crumb = m.groupdict()['crumb']
            crumb = crumb.replace(u'\\u002F', '/')
    return cookie, crumb  # return a tuple of crumb and cookie


def downloadFileFromYahoo(startDate, endDate, instrumentId, fileName, event='history'):
    logInfo('Downloading %s' % fileName)
    cookie, crumb = getCookieForYahoo(instrumentId)
    start = int(mktime(startDate.timetuple()))
    end = int(mktime(endDate.timetuple()))
    url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=%s&crumb=%s' % (instrumentId, start, end, event, crumb)
    data = requests.get(url, cookies={'B': cookie})
    with open(fileName, 'wb') as f:
        f.write(data.content)
        return True
    return False

'''
Takes list of instruments.
Outputs them grouped by and sorted by time:
ie [[t1, [i1,i2,i3]],
    [t2, [i4]],
    [t3, [i5, i6]] ], where t1<t2<t3
'''
def groupAndSortByTimeUpdates(instrumentUpdates):
    instrumentUpdates.sort(key=lambda x: x.getTimeOfUpdate())
    groupedInstruments = []
    timeUpdates = []
    # groupby only works on already sorted elements, so we sorted first
    for timeOfUpdate, sameTimeInstruments in groupby(instrumentUpdates, lambda x: x.getTimeOfUpdate()):
        instruments = []
        timeUpdates.append(timeOfUpdate)
        for sameTimeInstrument in sameTimeInstruments:
            instruments.append(sameTimeInstrument)
        groupedInstruments.append([timeOfUpdate, instruments])
    return timeUpdates, groupedInstruments

def getAllTimeStamps(groupedInstrumentUpdates):
    timeUpdates = []
    for timeOfUpdate, instrumentUpdates in groupedInstrumentUpdates:
        timeUpdates.append(timeOfUpdate)
    return timeUpdates

def getMultipliers(self,instrumentId, fileName, downloadId):
        divFile = self.getFileName('div', instrumentId)
        splitFile = self.getFileName('split', instrumentId)
        if not (os.path.isfile(divFile) and os.path.isfile(splitFile)):
            self.ensureDirectoryExists('div')
            self.ensureDirectoryExists('split')
            downloadFileFromYahoo(self.startDate, self.endDate, '%s%s'%(instrumentId,downloadId), divFile, event='div')
            downloadFileFromYahoo(self.startDate, self.endDate, '%s%s'%(instrumentId,downloadId), splitFile, event='split')
        div = pd.read_csv(divFile, engine='python', index_col='Date', parse_dates=True)
        split = pd.read_csv(splitFile, engine='python', index_col='Date', parse_dates=True)
        prices = pd.read_csv(fileName, engine='python', index_col='Date', parse_dates=True)
        temp = pd.concat([div, prices], axis=1).fillna(0)
        interim = (temp['Close'] - temp['Dividends']) / temp['Close']
        multiplier1 = interim.sort_index(ascending=False).cumprod().sort_index(ascending=True)
        temp2 = split['Stock Splits'].str.split('/', expand=True)
        if len(temp2.index) > 0:
            temp_mult = pd.to_numeric(temp2[1]) / pd.to_numeric(temp2[0])
            multiplier2 = temp_mult.sort_index(ascending=False).cumprod().sort_index(ascending=True)
        else:
            multiplier2 = pd.Series(1, index=multiplier1.index)
        multiplier = pd.concat([multiplier1, multiplier2], axis=1).fillna(method='bfill').fillna(1)
        multiplier[1] = multiplier[1].shift(-1).fillna(1)
        return multiplier
