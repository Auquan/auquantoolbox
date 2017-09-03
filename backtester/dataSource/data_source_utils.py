from datetime import datetime
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from data_source import DataSource
import os
import os.path
import requests
import re
try:
    from urllib import urlretrieve, urlopen
except ImportError:
    from urllib.request import urlretrieve, urlopen
from time import mktime as mktime
import pandas as pd

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
    logInfo('Downloading %s'%fileName)  
    cookie, crumb = getCookieForYahoo(instrumentId)
    start = int(mktime(startDate.timetuple()))
    end = int(mktime(endDate.timetuple()))
    url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=%s&crumb=%s'%(instrumentId, start, end, event,crumb)
    data = requests.get(url, cookies={'B':cookie})
    with open(fileName,'w') as f:
        f.write(data.content)