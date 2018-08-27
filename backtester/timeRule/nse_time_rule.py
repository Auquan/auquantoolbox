from backtester.timeRule.custom_time_rule import CustomTimeRule
from datetime import datetime, timedelta
import os
import os.path
import csv
from bs4 import BeautifulSoup
try:
    from urllib.request import Request, urlopen, HTTPError  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, HTTPError  # Python 2


class NSETimeRule(CustomTimeRule):
    def __init__(self, startDate, endDate, startTime='9:30', endTime='15:30', frequency='H', sample='1'):
        super(NSETimeRule, self).__init__(startDate = startDate, endDate = endDate, startTime = startTime, endTime= endTime, holidays = self.getNSEHolidays(), frequency = frequency, sample = sample)

    def getNSEHolidays(self):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.8',
               'Host': 'nseindia.com',
               'Connection': 'keep-alive',
               'Referer': 'https://www.nseindia.com/products/content/equities/equities/mrkt_timing_holidays.htm',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'X-Requested-With': 'XMLHttpRequest'}
        #May possibly break on 1st january in case NSE does not post the holidays for the new year on time
        fromDate = (datetime(2010, 1, 1)).strftime("%d-%m-%Y")
        toDate = datetime(datetime.now().year, 12, 31).strftime("%d-%m-%Y")
        url = 'https://www.nseindia.com/global/content/market_timings_holidays/market_timings_holidays.jsp?pageName=0&dateRange=&fromDate=%s&toDate=%s&tabActive=trading&load=false' % (fromDate,toDate) 
        req = Request(url, headers=hdr)
        try:
            page = urlopen(req)
            content = page.read().decode('utf8')
            soup = BeautifulSoup(content, 'lxml')
            holidays = [datetime.strptime(date.get_text(), '%d-%b-%Y') for date in soup.find_all(class_="number")]
            return holidays
        except HTTPError as e:
            print(e.fp.read())
            return None
