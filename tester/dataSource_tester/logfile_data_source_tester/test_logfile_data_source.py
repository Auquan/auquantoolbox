import os,sys,shutil,pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, time, timedelta
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.logfile_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from data_logfile_data_source import *

def test_logfile_data_source():
    for i in range(0,1):
        data = data_logfile_data_source(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        os.makedirs(os.path.dirname(parameters["fileName"]), exist_ok=True)
        with open(parameters["fileName"], 'w') as f:
            f.write("AAA\nBBB\nCCC\n")
        logfiledatasource=LogfileDataSource(parameters["fileName"],parameters["liveUpdates"])
        assert LogfileDataSource.processLineIntoInstrumentUpdate(logfiledatasource,parameters["line"]) == results["line"]
        assert LogfileDataSource.processLine(logfiledatasource,parameters["line"]).getFutureInstrumentId()==results["getFutureInstrumentId"]
        assert LogfileDataSource.processLine(logfiledatasource,parameters["line"]).getTypeOfInstrument()==results["getTypeOfInstrument"]
        assert LogfileDataSource.processLine(logfiledatasource,parameters["line"]).getExpiryTime()==results["getExpiryTime"]
        assert LogfileDataSource.processLine(logfiledatasource,parameters["line"]).getUnderlyingInstrumentId()==results["getUnderlyingInstrumentId"]

######## issue with emitInstrumentUpdates as for liveUpdates=False
        """
        ele=logfiledatasource.emitInstrumentUpdates()
        for c in range(0,i+1):
            with open(parameters["fileName"], 'a+') as f:
                f.write("AAA\n")
                #inst=next(ele)
                #print (inst)
                assert isinstance(next(ele),FutureInstrumentUpdate)
                #assert isinstance(inst,FutureInstrumentUpdate)
        """
        shutil.rmtree(parameters["folderName"])
