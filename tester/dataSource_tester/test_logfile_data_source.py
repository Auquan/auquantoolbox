import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.dataSource.logfile_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from datetime import datetime, time, timedelta
import time
import multiprocessing
from unittest.mock import Mock, MagicMock
import pytest
import signal
from initializeds import Initialize
import os

def test_logfile_data_source():
        initialize=Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                os.makedirs(os.path.dirname(parameters["fileNameforlogfile"]), exist_ok=True)
                with open(parameters["fileNameforlogfile"], 'w') as f:
                        f.write("AAA")
                        f.write("\n")
                        f.write("BBB")
                        f.write("\n")
                        f.write("CCC")
                        f.write("\n")
                logfiledatasource=LogfileDataSource(parameters["fileNameforlogfile"],parameters["liveUpdates"])
                assert LogfileDataSource.processLineIntoInstrumentUpdate(logfiledatasource,"ABC") == "ABC"
                ele=logfiledatasource.emitInstrumentUpdates()
                for c in range(0,i):
                    with open(parameters["fileNameforlogfile"], 'a+') as f:
                            f.write("AAA")
                            f.write("\n")
                    assert isinstance(next(ele),FutureInstrumentUpdate)
                shutil.rmtree(parameters["cachedFolderName"])
