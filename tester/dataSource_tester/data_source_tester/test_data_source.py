import os,sys,shutil,pytest,pandas as pd
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.data_source import DataSource
from backtester.dataSource.csv_data_source import *
from backtester.logger import *
from data_data_source import *

def test_data_source():
    for i in range(0,3):
        data = data_data_source(i)
        parameters=data["parameters"]
        results=data["results"]
        dataSet=data["dataSet"]
######## testing for DataSource Class
        if i==0 or i==1:
            datasource=DataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                  parameters["instrumentIds"],parameters["startDateStr"],
                                  parameters["endDateStr"])
        if i==2:
            with pytest.raises(NotImplementedError):
                datasource=DataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                      parameters["instrumentIds"],parameters["startDateStr"],
                                      parameters["endDateStr"])
        if i==0 or i==1:
            with pytest.raises(NotImplementedError):
                DataSource.getInstrumentUpdateFromRow(datasource,parameters["dataSetId"],"")
            with pytest.raises(NotImplementedError):
                DataSource.downloadAndAdjustData(datasource,parameters["dataSetId"],parameters["fileName"])
            with pytest.raises(NotImplementedError):
                DataSource.getAllInstrumentIds(datasource)
        if i==0 or i==1:
            assert DataSource.getInstrumentIds(datasource) == results["getInstrumentIds"]
            assert DataSource.getBookDataFeatures(datasource) == None
            assert list(DataSource.emitInstrumentUpdates(datasource))==[]
            assert DataSource.emitAllInstrumentUpdates(datasource)==None

##############  creating CsvDataSource object to test derived functions

            csvdatasource=CsvDataSource(parameters["cachedFolderName"],parameters["dataSetId"],
                                        parameters["instrumentIds"],parameters["downloadUrl"],
                                        parameters["timeKey"],parameters["timeStringFormat"],
                                        parameters["startDateStr"],parameters["endDateStr"],
                                        parameters["liveUpdates"],parameters["pad"])
            result_timeUpdates,result_groupedInstrumentUpdates=DataSource.getGroupedInstrumentUpdates(csvdatasource)
            assert result_timeUpdates==results["timeUpdates_getGroupedInstrumentUpdates"]
            list_timeUpdates=[]
            list_getStockInstrumentId=[]
            list_getTypeOfInstrument=[]
            for ele in result_groupedInstrumentUpdates:
                list_timeUpdates.append(ele[0])
                list_getStockInstrumentId.append(ele[1][0].getStockInstrumentId())
                list_getTypeOfInstrument.append(ele[1][0].getTypeOfInstrument())
            assert list_timeUpdates==results["timeUpdates_getGroupedInstrumentUpdates"]
            assert list_getStockInstrumentId==results["list_getStockInstrumentId"]
            assert list_getTypeOfInstrument==results["list_getTypeOfInstrument"]
            result_timeUpdates,result_allInstrumentUpdates=DataSource.getAllInstrumentUpdates(csvdatasource)
            assert result_timeUpdates==results["timeUpdates_getAllInstrumentUpdates"]
            for inst in parameters["instrumentIds"]:
                result_allInstrumentUpdates[inst].equals(dataSet["dsdict_getAllInstrumentUpdates"][inst])
            csvdatasource._bookDataByInstrument=result_allInstrumentUpdates
            csvdatasource.padInstrumentUpdates()
            for inst in parameters["instrumentIds"]:
                assert csvdatasource._bookDataByInstrument[inst].round(3).equals(dataSet["dsdict_padInstrumentUpdates"][inst])
            csvdatasource.processAllInstrumentUpdates()
            for inst in parameters["instrumentIds"]:
                if i==0:
                    #checking column by column because the orientation of the columns is not same for everyrun
                    for ele in csvdatasource._bookDataByInstrument[inst]:
                        assert csvdatasource._bookDataByInstrument[inst][ele].round(3).equals(dataSet["dsdict_processAllInstrumentUpdates"][inst][ele])
                if i==1:
                    assert csvdatasource._bookDataByInstrument[inst].equals(dataSet["dsdict_processAllInstrumentUpdates"][inst])
            csvdatasource.filterUpdatesByDates([(parameters["startDateStr_filterUpdatesByDates"], parameters["endDateStr_filterUpdatesByDates"])])
            for inst in parameters["instrumentIds"]:
                if i==0:
                    #checking column by column because the orientation of the columns is not same for everyrun
                    for ele in csvdatasource._bookDataByInstrument[inst]:
                        assert csvdatasource._bookDataByInstrument[inst][ele].round(3).equals(dataSet["dsdict_processAllInstrumentUpdates"][inst][ele])
                if i==1:
                    assert csvdatasource._bookDataByInstrument[inst].equals(dataSet["dsdict_processAllInstrumentUpdates"][inst])
            if i==0:
                datasource.setStartDate(parameters["startDateStr"])
                assert datasource._startDate==results["setStartDate"]
                datasource.setEndDate(parameters["endDateStr"])
                assert datasource._endDate==results["setEndDate"]
                datasource.setDateRange([(parameters["startDateStr_filterUpdatesByDates"], parameters["endDateStr_filterUpdatesByDates"])])
                assert datasource._dateRange==results["setDateRange"]
                DataSource.ensureDirectoryExists(datasource,parameters["cachedFolderName"],parameters["dataSetId"])
                assert os.path.exists(parameters["cachedFolderName"])
                assert os.path.exists(parameters["cachedFolderName"]+'/'+parameters["dataSetId"])
                DataSource.cleanup(datasource)
        shutil.rmtree(parameters["cachedFolderName"])
