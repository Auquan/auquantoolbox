from backtester.dataSource.csv_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
import os,sys,shutil
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
import pytest
from initialize import Initialize

def test_datasource():
        initialize=Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                assert is_number(parameters["s"]==results["is_number"])
                csvdatasource=CsvDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                            parameters["instrumentIds"],parameters["downloadUrl"],
                                            parameters["timeKey"],parameters["timeStringFormat"],
                                            parameters["startDateStr"],parameters["endDateStr"],
                                            parameters["liveUpdates"],parameters["pad"])
                assert CsvDataSource.getFileName(csvdatasource,parameters["instrumentIdforcsv"])==results["getFileNameforcsv"]
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
                assert CsvDataSource.getAllInstrumentIds(csvdatasource) == results["getAllInstrumentIds"]
                assert CsvDataSource.downloadFile(csvdatasource,parameters["instrumentIdforcsv"],results["getFileNameforcsv"])==results["ensureAllInstrumentsFile"]
                check(parameters["cachedFolderName"],parameters["dataSetId"],parameters["instrumentIdforcsv"])
                assert CsvDataSource.downloadAndAdjustData(csvdatasource,parameters["instrumentIdforcsv"],results["getFileNameforcsv"])==results["ensureAllInstrumentsFile"]
                dict=[]
                for row in data["records"]:
                        resultinst=CsvDataSource.getInstrumentUpdateFromRow(csvdatasource,parameters["instrumentIdforcsv"],row)
                        dict.append(resultinst)
                count=0
                for i in dict:
                        count+=1
                        assert isinstance(i,StockInstrumentUpdate)
                assert count == 4
                shutil.rmtree(parameters["cachedFolderName"])
