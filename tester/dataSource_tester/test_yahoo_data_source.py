import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.dataSource.yahoo_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from initializeds import Initialize
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import pytest
import os
import numpy as np
import pandas as pd

def test_yahoo_data_source():
    initialize=Initialize()
    for i in range(0,4):
        dataSet = initialize.getDataSet(i)
        data=dataSet["dataSet"]
        parameters=dataSet["parameters"]
        results=dataSet["results"]
        assert checkDate(parameters["lineItem"]) == results["checkDateYahoo"]
        assert checkTimestamp(parameters["lineItem"]) == True
        assert validateLineItem(parameters["lineItems"]) == results["validateLineItemYahoo"]

    for i in range(0,3):
        dataSet = initialize.getDataSet(i)
        data=dataSet["dataSet"]
        parameters=dataSet["parameters"]
        results=dataSet["results"]
        assert parseDataLine(parameters["lineItems"]) == results["parseDataLineYahoo"]

    for i in range(3,4):
        dataSet = initialize.getDataSet(i)
        data=dataSet["dataSet"]
        parameters=dataSet["parameters"]
        results=dataSet["results"]
        with pytest.raises(ValueError):
            parseDataLine(parameters["lineItems"])
    assert is_number('a') == False
    assert is_number(90) == True
    p = {1:['Open','open'],2:['Close','close'],3:['High','high'],4:['Low','low']}
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2017/12/21'
    endDateStr = '2018/01/31'
    startDateStrp = '2017/12/25'
    yds = YahooStockDataSource(cachedFolderName='yahooData/',dataSetId="testTrading",
                                     instrumentIds=instrumentIds,startDateStr=startDateStrp,
                                     endDateStr=startDateStrp,event='history',
                                     liveUpdates=True)
    bd1 = {'open': 1.0,'high': 1.0,'low': 1.0,'close': 1.0,'Adj Close' : 1.0,'volume': 1.0}
    bd = {'open': 1.0,'high': 1.0,'low': np.nan,'close': 1.0,'Adj Close' : 1.0,'volume': 1.0}
    yds._allTimes = ['2017/12/20', '2017/12/21']
    od=OrderedDict()
    od['IBM']=1.0
    od['AAPL']=1.0
    a = pd.DataFrame(data=od, index = ['2017/12/20', '2017/12/21'])
    yds._groupedInstrumentUpdates = [['2017/12/20',[StockInstrumentUpdate('IBM','IBM','2017/12/20', bd1),StockInstrumentUpdate('AAPL','AAPL','2017/12/20', bd1)]],
                                     ['2017/12/21',[StockInstrumentUpdate('IBM','IBM','2017/12/21', bd),StockInstrumentUpdate('AAPL','AAPL','2017/12/21', bd)]]]
    YahooStockDataSource.processGroupedInstrumentUpdates(yds)
    b=YahooStockDataSource.getBookDataByFeature(yds)
    for i in b:
        assert b[i].equals(a) == True
    assert YahooStockDataSource.getClosingTime(yds) == '2017/12/21'
    assert YahooStockDataSource.getFileName(yds,'IBM') == 'yahooData/testTrading/IBM_2017-12-25to2017-12-25.csv'
    rowe = {'Open': 1,'High': 2,'Low': 3,'Close': 4,'Adj Close' : 5,'Volume': 6,'Date' : '2011-02-21'}
    assert isinstance(YahooStockDataSource.getInstrumentUpdateFromRow(yds, 'IBM', rowe),StockInstrumentUpdate) == True

    yds1 = YahooStockDataSource(cachedFolderName='yahooData1/',dataSetId="testTrading",
                                     instrumentIds=['AAPL'],startDateStr='2018/07/30',
                                     endDateStr='2018/08/11',event='history', adjustPrice = False,
                                     liveUpdates=True)
    YahooStockDataSource.adjustPriceForSplitAndDiv(yds1, 'AAPL', 'yahooData1/testTrading/AAPL_2018-07-30to2018-08-11.csv')
    a = pd.read_csv('yahooData1/testTrading/AAPL_2018-07-30to2018-08-11.csv', engine='python', index_col='Date', parse_dates=True)
    b=YahooStockDataSource.getBookDataByFeature(yds1)
    for i in p:
        q = (a[p[i][0]].values)/(b[p[i][1]]['AAPL'].values)
        assert np.unique(np.round(q,2)).size == 1
    shutil.rmtree('yahooData')
    shutil.rmtree('yahooData1')
