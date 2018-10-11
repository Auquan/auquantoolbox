import os,sys,shutil,pytest
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.csv_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from data_csv_data_source import *

def test_csv_data_source():
    for i in range(0,6):
        data = data_csv_data_source(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        if i in range (0,3):
            assert is_number(parameters["s"]==results["is_number"])
######## testing for CsvDataSource Class
        csvdatasource=CsvDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                    parameters["instrumentIds"],parameters["downloadUrl"],
                                    parameters["timeKey"],parameters["timeStringFormat"],
                                    parameters["startDateStr"],parameters["endDateStr"],
                                    parameters["liveUpdates"],parameters["pad"])
        if i==0:
            assert CsvDataSource.getFileName(csvdatasource,parameters["instrumentId"])==results["getFileName"]
        if i==0 or i==3:
            assert CsvDataSource.ensureAllInstrumentsFile(csvdatasource,parameters["dataSetId"])==results["ensureAllInstrumentsFile"]
        def check(folder,id,inst):
            pathtofile="%s/%s/%s.csv" %(folder,id,inst)
            if os.path.exists(pathtofile):
                with open (pathtofile,'r') as f:
                        content=f.read()
                url="https://raw.githubusercontent.com/Auquan/test_repo/master/%s/%s.csv" %(id,inst)
                response=urlopen(url)
                datafromgithub=response.read().decode('utf8')
                assert datafromgithub==content
        for inst in parameters["instrumentIds"]:
            check(parameters["cachedFolderName"],parameters["dataSetId"],inst)
        if i==0 or i==3:
            assert CsvDataSource.getAllInstrumentIds(csvdatasource) == results["getAllInstrumentIds"]
        if i in range (0,4):
            assert CsvDataSource.downloadFile(csvdatasource,parameters["instrumentId"],parameters["getFileName"])==results["downloadFile"]
            check(parameters["cachedFolderName"],parameters["dataSetId"],parameters["instrumentId"])
            assert CsvDataSource.downloadAndAdjustData(csvdatasource,parameters["instrumentId"],parameters["getFileName"])==results["downloadAndAdjustData"]
            check(parameters["cachedFolderName"],parameters["dataSetId"],parameters["instrumentId"])
        if i==0 or i==1:
            list=[]
            for row in dataSet["records"]:
                resultinst=CsvDataSource.getInstrumentUpdateFromRow(csvdatasource,parameters["instrumentId"],row)
                list.append(resultinst)
            listStockInstrumentId=[]
            listTypeOfInstrument=[]
            count=0
            for ele in list:
                count+=1
                assert isinstance(ele,StockInstrumentUpdate)
                listStockInstrumentId.append(ele.getStockInstrumentId())
                listTypeOfInstrument.append(ele.getTypeOfInstrument())
            assert count == results["count"]
            assert listStockInstrumentId==results["listStockInstrumentId"]
            assert listTypeOfInstrument==results["listTypeOfInstrument"]
        shutil.rmtree(parameters["cachedFolderName"])
