from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
import requests
import re
from time import mktime as mktime


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
