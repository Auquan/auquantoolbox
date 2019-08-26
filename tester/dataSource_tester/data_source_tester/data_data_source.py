import pandas as pd
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
######## testing for DataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['AAE', 'AGG']
        parameters["startDateStr"]='2018/01/01'
        parameters["endDateStr"]='2018/02/01'
        parameters["fileName"]="Folder1/data.txt"
######## testing for getInstrumentIds
        results["getInstrumentIds"]=['AAE', 'AGG']
######## parameters for CsvDataSource Class
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]="datetime"
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["liveUpdates"]=True
        parameters["pad"]=True
######## testing for getGroupedInstrumentUpdates
        results["timeUpdates_getGroupedInstrumentUpdates"]=[datetime(2010, 6, 2, 9, 20),
                                                            datetime(2010, 6, 2, 9, 25),
                                                            datetime(2010, 12, 24, 15, 30),
                                                            datetime(2010, 12, 27, 9, 20)]
        results["list_getStockInstrumentId"]=['AAE', 'AAE', 'AGG', 'AGG']
        results["list_getTypeOfInstrument"]=['stock', 'stock', 'stock', 'stock']
######## testing for getAllInstrumentUpdates
        results["timeUpdates_getAllInstrumentUpdates"]=[pd.Timestamp('2010-06-02 09:20:00'),
                                                        pd.Timestamp('2010-06-02 09:25:00'),
                                                        pd.Timestamp('2010-12-24 15:30:00'),
                                                        pd.Timestamp('2010-12-27 09:20:00')]
        dataSet["dsdict_getAllInstrumentUpdates"]={"AAE":pd.DataFrame({'F0':[48.124,48.189],'F1':[0.297,0.297],'F2':[-0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00')]),
                                                   "AGG":pd.DataFrame({'F0':[128.326,127.607],'F1':[0.503,0.500]}, index=[pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## testing for padInstrumentUpdates
        dataSet["dsdict_padInstrumentUpdates"]={"AAE":pd.DataFrame({'F0':[48.124,48.189,48.189,48.189],'F1':[0.297,0.297,0.297,0.297],'F2':[-0.1,0.1,0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                                "AGG":pd.DataFrame({'F0':[0.00,0.00,128.326,127.607],'F1':[0.00,0.00,0.503,0.500]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## testing for processAllInstrumentUpdates
        dataSet["dsdict_processAllInstrumentUpdates"]={"AAE":pd.DataFrame({'F0':[48.124,48.189,48.189,48.189],'F1':[0.297,0.297,0.297,0.297],'F2':[-0.1,0.1,0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                                       "AGG":pd.DataFrame({'F0':[0.00,0.00,128.326,127.607],'F1':[0.00,0.00,0.503,0.500]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## testing for setstartDate, setEndDate and setDateRange
        parameters["startDateStr_filterUpdatesByDates"]="2010/06/02"
        parameters["endDateStr_filterUpdatesByDates"]="2010/12/27"
        results["setStartDate"]=datetime(2018, 1, 1, 0, 0)
        results["setEndDate"]=datetime(2018, 2, 1, 0, 0)
        results["setDateRange"]=[('2010/06/02', '2010/12/27')]

    if c==1:
######## testing for DataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        parameters["instrumentIds"]=['AAE', 'AGG']
        parameters["startDateStr"]='2018/01/01'
        parameters["endDateStr"]='2018/02/01'
        parameters["fileName"]="Folder1/data.txt"
######## testing for getInstrumentIds
        results["getInstrumentIds"]=['AAE', 'AGG']
######## parameters for CsvDataSource Class
        parameters["downloadUrl"]="https://raw.githubusercontent.com/Auquan/test_repo/master"
        parameters["timeKey"]="datetime"
        parameters["timeStringFormat"]="%Y-%m-%d %H:%M:%S"
        parameters["liveUpdates"]=False
        parameters["pad"]=True
######## testing for getGroupedInstrumentUpdates
        results["timeUpdates_getGroupedInstrumentUpdates"]=[datetime(2010, 6, 2, 9, 20),
                                                            datetime(2010, 6, 2, 9, 25),
                                                            datetime(2010, 12, 24, 15, 30),
                                                            datetime(2010, 12, 27, 9, 20)]
        results["list_getStockInstrumentId"]=['AAE', 'AAE', 'AGG', 'AGG']
        results["list_getTypeOfInstrument"]=['stock', 'stock', 'stock', 'stock']
######## testing for getAllInstrumentUpdates
        results["timeUpdates_getAllInstrumentUpdates"]=[pd.Timestamp('2010-06-02 09:20:00'),
                                                        pd.Timestamp('2010-06-02 09:25:00'),
                                                        pd.Timestamp('2010-12-24 15:30:00'),
                                                        pd.Timestamp('2010-12-27 09:20:00')]
        dataSet["dsdict_getAllInstrumentUpdates"]={"AAE":pd.DataFrame({'F0':[48.124,48.189],'F1':[0.297,0.297],'F2':[-0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00')]),
                                                   "AGG":pd.DataFrame({'F0':[128.326,127.607],'F1':[0.503,0.500]}, index=[pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## testing for padInstrumentUpdates
        dataSet["dsdict_padInstrumentUpdates"]={"AAE":pd.DataFrame({'F0':[48.124,48.189,48.189,48.189],'F1':[0.297,0.297,0.297,0.297],'F2':[-0.1,0.1,0.1,0.1]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                                "AGG":pd.DataFrame({'F0':[0.00,0.00,128.326,127.607],'F1':[0.00,0.00,0.503,0.500]}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## testing for processAllInstrumentUpdates
        dataSet["dsdict_processAllInstrumentUpdates"]={"AAE":pd.DataFrame({}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')]),
                                                       "AGG":pd.DataFrame({}, index=[pd.Timestamp('2010-06-02 09:20:00'),pd.Timestamp('2010-06-02 09:25:00'),pd.Timestamp('2010-12-24 15:30:00'),pd.Timestamp('2010-12-27 09:20:00')])}
######## parameters for setstartDate, setEndDate
        parameters["startDateStr_filterUpdatesByDates"]="2010/06/02"
        parameters["endDateStr_filterUpdatesByDates"]="2010/12/27"

    if c==2:
######## testing for DataSource Class
        parameters["cachedFolderName"]="Folder1/"
        parameters["dataSetId"]="QQ3Data"
        # no instrumentIds provided
        parameters["instrumentIds"]=[]
        parameters["startDateStr"]='2018/01/01'
        parameters["endDateStr"]='2018/02/01'
        parameters["fileName"]="Folder1/data.txt"
######## testing for getInstrumentIds
        results["getInstrumentIds"]=[]

    return {"dataSet":dataSet,"parameters":parameters,"results":results}
