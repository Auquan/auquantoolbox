from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
import requests
import re
from time import mktime as mktime
from itertools import groupby


def getCookieForYahoo(instrumentId):
    """Returns a tuple pair of cookie and crumb used in the request"""
    url = 'https://finance.yahoo.com/quote/%s/history' % (instrumentId)
    r = requests.get(url)
    txt = r.content
    cookie = r.cookies['B']
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
    with open(fileName, 'w') as f:
        f.write(data.content)


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
    # groupby only works on already sorted elements, so we sorted first
    for timeOfUpdate, sameTimeInstruments in groupby(instrumentUpdates, lambda x: x.getTimeOfUpdate()):
        instruments = []
        for sameTimeInstrument in sameTimeInstruments:
            instruments.append(sameTimeInstrument)
        groupedInstruments.append([timeOfUpdate, instruments])
    return groupedInstruments
