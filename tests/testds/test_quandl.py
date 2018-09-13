import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.dataSource.quandl_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from initializeds import Initialize
from datetime import datetime, time, timedelta
from collections import OrderedDict
from unittest.mock import Mock, MagicMock
import pytest
import pandas as pd
import numpy as np

def test_quandlDataSource():
    initialize=Initialize()
    for i in range(0,4):
        dataSet = initialize.getDataSet(i)
        data=dataSet["dataSet"]
        parameters=dataSet["parameters"]
        results=dataSet["results"]
        assert checkDate(parameters["lineItem"]) == results["checkDateYahoo"]
        assert is_number('a') == False
        assert is_number(90) == True
    instrumentIds = ['IBM', 'AAPL']
    startDateStr = '2013/05/10'
    endDateStr = '2013/05/15'
    startDateStrp = '2017/12/25'
    qds = QuandlDataSource(cachedFolderName='Folder1/',dataSetId="testTrading",
                                     instrumentIds=instrumentIds,startDateStr=startDateStr,
                                     endDateStr=endDateStr,liveUpdates=False)
    assert QuandlDataSource.downloadFile(qds, 'IBM', 'Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == True
    assert os.path.isfile('Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == True
    shutil.rmtree('Folder1')
    assert QuandlDataSource.downloadFile(qds, 'GOA', 'Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == False
    assert os.path.isfile('Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == False
    qds = QuandlDataSource(cachedFolderName='Folder1/',dataSetId="testTrading",
                                     instrumentIds=instrumentIds,startDateStr=startDateStr,
                                     endDateStr=endDateStr,liveUpdates=False)
    assert QuandlDataSource.downloadAndAdjustData(qds, 'IBM', 'Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == True
    assert os.path.isfile('Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == True
    shutil.rmtree('Folder1')
    assert QuandlDataSource.downloadAndAdjustData(qds, 'GOA', 'Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == False
    assert os.path.isfile('Folder1/testTrading/IBM_2013-05-10to2017-06-09.csv') == False
    rowe = {'Open': 1,'High': 2,'Low': 3,'Close': 4,'Adj Close' : 5,'Volume': 6,
                'Date' : '2011-02-21'}
    result = QuandlDataSource.getInstrumentUpdateFromRow(qds, 'IBM', rowe)
    assert isinstance(result, StockInstrumentUpdate) == True
    assert result.getBookData() == {'Open': 1, 'High': 2, 'Low': 3, 'Close': 4, 'Adj Close' : 5, 'Volume': 6}
    assert result.getTimeOfUpdate() == datetime(2011, 2, 21, 0, 0)
    qds1 = QuandlDataSource(cachedFolderName='Folder2/',dataSetId="testTrading",
                                     instrumentIds=instrumentIds,startDateStr=startDateStrp,
                                     endDateStr=startDateStrp,
                                     liveUpdates=True)
    bd1 = {'open': 1.0,'high': 1.0,'low': 1.0,'close': 1.0,'Adj Close' : 1.0,'volume': 1.0}
    bd = {'open': 1.0,'high': 1.0,'low': np.nan,'close': 1.0,'Adj Close' : 1.0,'volume': 1.0}
    qds1._allTimes = ['2017/12/20', '2017/12/21']
    od=OrderedDict()
    od['IBM']=1.0
    od['AAPL']=1.0
    a = pd.DataFrame(data=od, index = ['2017/12/20', '2017/12/21'])
    qds1._groupedInstrumentUpdates = [['2017/12/20',[StockInstrumentUpdate('IBM','IBM','2017/12/20', bd1),StockInstrumentUpdate('AAPL','AAPL','2017/12/20', bd1)]],
                                     ['2017/12/21',[StockInstrumentUpdate('IBM','IBM','2017/12/21', bd),StockInstrumentUpdate('AAPL','AAPL','2017/12/21', bd)]]]
    QuandlDataSource.processGroupedInstrumentUpdates(qds1)

    b=QuandlDataSource.getBookDataByFeature(qds1)
    for i in b:
        assert b[i].equals(a) == True
    shutil.rmtree('Folder2')
