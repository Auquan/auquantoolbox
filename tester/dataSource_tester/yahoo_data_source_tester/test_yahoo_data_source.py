import os,sys,shutil,numpy as np,pandas as pd,pytest
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
from collections import OrderedDict
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.yahoo_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from data_yahoo_data_source import *

def test_yahoo_data_source():
    for i in range(0,4):
        data = data_yahoo_data_source(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        assert checkDate(parameters["lineItem"]) == results["checkDate"]
        assert checkTimestamp(parameters["lineItem"]) == True
        assert validateLineItem(parameters["lineItems"]) == results["validateLineItem"]
        if i in range(0,3):
            data = data_yahoo_data_source(i)
            dataSet=data["dataSet"]
            parameters=data["parameters"]
            results=data["results"]
            assert parseDataLine(parameters["lineItems"]) == results["parseDataLine"]
            assert isFloat(parameters["s"])==results["isFloat"]
            assert is_number(parameters["s"]) == results["is_number"]
        if i==3:
            data = data_yahoo_data_source(i)
            dataSet=data["dataSet"]
            parameters=data["parameters"]
            results=data["results"]
            with pytest.raises(ValueError):
                parseDataLine(parameters["lineItems"])
        if i==0:
            yds = YahooStockDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                       parameters["instrumentIds"],"2017/12/25",
                                       "2017/12/25",parameters["event"],
                                       parameters["adjustPrice"],parameters["downloadId"],
                                       parameters["liveUpdates"],parameters["pad"])
            p = {1:['Open','open'],2:['Close','close'],3:['High','high'],4:['Low','low']}
            startDateStrp = '2017/12/25'
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
