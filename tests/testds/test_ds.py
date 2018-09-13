import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.dataSource.data_source import DataSource
from backtester.dataSource.csv_data_source import *
from backtester.logger import *
import pandas as pd
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
import pytest
from initializeds import Initialize

def test_datasource():
        initialize=Initialize()
        for i in range(0,1):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                data=dataSet["dataSet"]
                datasource=DataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                      parameters["instrumentIds"],parameters["startDateStr"],
                                      parameters["endDateStr"])
                csvdatasource1=CsvDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                             parameters["instrumentIds"],parameters["downloadUrl"],
                                             parameters["timeKey"],parameters["timeStringFormat"],
                                             parameters["startDateStr"],parameters["endDateStr"],
                                             True,parameters["pad"])
                csvdatasource2=CsvDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                             parameters["instrumentIds"],parameters["downloadUrl"],
                                             parameters["timeKey"],parameters["timeStringFormat"],
                                             parameters["startDateStr"],parameters["endDateStr"],
                                             False,parameters["pad"])
                with pytest.raises(NotImplementedError):
                        DataSource.getInstrumentUpdateFromRow(datasource,parameters["dataSetId"],"")
                with pytest.raises(NotImplementedError):
                        DataSource.downloadAndAdjustData(datasource,parameters["dataSetId"],parameters["fileName"])
                with pytest.raises(NotImplementedError):
                        DataSource.getAllInstrumentIds(datasource)
                resultgetInstrumentIds=DataSource.getInstrumentIds(datasource)
                assert resultgetInstrumentIds == results["getInstrumentIds"]
                assert DataSource.getBookDataFeatures(datasource) == None
                resultemitInstrumentUpdates=DataSource.emitInstrumentUpdates(datasource)
                assert DataSource.emitAllInstrumentUpdates(datasource)==None
                resulttimeUpdatesforgetGrouped,resultgroupedInstrumentUpdatesforgetGrouped=DataSource.getGroupedInstrumentUpdates(csvdatasource1)
                resulttimeUpdatesforgetAll,resultgroupedInstrumentUpdatesforgetAll=DataSource.getAllInstrumentUpdates(csvdatasource1)
                assert resulttimeUpdatesforgetGrouped==results["resulttimeUpdatesforgetGrouped"]
                datelist=[]
                for ele in resultgroupedInstrumentUpdatesforgetGrouped:
                        datelist.append(ele[0])
                        assert isinstance(ele[1][0],StockInstrumentUpdate)
                assert datelist==results["resulttimeUpdatesforgetGrouped"]
                assert (resulttimeUpdatesforgetAll,results["resulttimeUpdatesforgetGrouped"])
                for inst in parameters["instrumentIds"]:
                        df=pd.read_csv("https://raw.githubusercontent.com/Auquan/test_repo/master/QQ3Data/%s.csv"%(inst))
                        df=df.set_index('datetime')
                        assert df.equals(resultgroupedInstrumentUpdatesforgetAll[inst])
                csvdatasource2._bookDataByInstrument=resultgroupedInstrumentUpdatesforgetAll
                csvdatasource2.padInstrumentUpdates()
                for inst in parameters["instrumentIds"]:
                        csvdatasource2._bookDataByInstrument[inst]=csvdatasource2._bookDataByInstrument[inst].round(3)
                        assert csvdatasource2._bookDataByInstrument[inst].equals(data["dsdict"]["%s"%(inst)])
                csvdatasource1.processAllInstrumentUpdates()
                for inst in parameters["instrumentIds"]:
                        csvdatasource1._bookDataByInstrument[inst]=csvdatasource1._bookDataByInstrument[inst].round(3)
                        for columns in csvdatasource1._bookDataByInstrument[inst]:
                                assert csvdatasource1._bookDataByInstrument[inst][columns].equals(data["dsdict"]["%s"%(inst)][columns])
                csvdatasource2.filterUpdatesByDates([(parameters["startDateStrforfilterUpdates"], parameters["endDateStrforfilterUpdates"])])
                for inst in parameters["instrumentIds"]:
                        csvdatasource2._bookDataByInstrument[inst]=csvdatasource2._bookDataByInstrument[inst].round(3)
                        assert csvdatasource2._bookDataByInstrument[inst].equals(data["dsdict"]["%s"%(inst)])
                datasource.setStartDate(parameters["startDateStr"])
                assert datasource._startDate==results["setStartDate"]
                datasource.setEndDate(parameters["endDateStr"])
                assert datasource._endDate==results["setEndDate"]
                datasource.setDateRange(parameters["dateRange"])
                assert datasource._dateRange==results["setDateRange"]
                DataSource.ensureDirectoryExists(datasource,parameters["cachedFolderName"],parameters["dataSetId"])
                assert os.path.exists(parameters["cachedFolderName"])
                assert os.path.exists(parameters["cachedFolderName"]+'/'+parameters["dataSetId"])
                DataSource.cleanup(datasource)
                shutil.rmtree(parameters["cachedFolderName"])
