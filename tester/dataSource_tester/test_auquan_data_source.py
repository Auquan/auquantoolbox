import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.dataSource.auquan_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
import pytest
from initializeds import Initialize
import os

def test_auquan_data_source():
        initialize=Initialize()
        for i in range(0,4):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                assert checkDate(parameters["lineItem"]) == results["checkDate"]
                assert checkTimestamp(parameters["lineItem"]) ==True
                assert validateLineItem(parameters["lineItems"]) ==results["validateLineItem"]
                assert parseBookDataOptionLine(parameters["lineItems"]) == results["parseBookDataOptionLine"]
                assert get_exp_date(parameters["trade_date"]) == results["get_exp_date"]
                auqundatasource=AuquanDataSource(parameters["cachedFolderName"],parameters["instrumentIdsByType"],
                                                 parameters["startDateStrforauquan"],parameters["endDateStrforauquan"],
                                                 parameters["liveUpdates"])
                assert AuquanDataSource.getFileName(auqundatasource,"a",parameters["instrumentId"],parameters["startDate"]) == results["getFileName"]
                if i==0:
                        os.makedirs(os.path.dirname('Folder1/b/BBA/BBA_20180102.txt'), exist_ok=True)
                        os.makedirs(os.path.dirname('Folder1/b/BPM/BPM_20180102.txt'), exist_ok=True)
                        with open('Folder1/b/BBA/BBA_20180102.txt', 'w') as f:
                                f.write('2017/01/01 09:30:00:000000 Book 100 AAA\n2018/01/01 09:30:00:000000 Book 100 AAA\n2019/01/01 09:30:00:000000 Book 100 AAA')
                        with open('Folder1/b/BPM/BPM_20180102.txt', 'w') as f:
                                f.write('2016/01/01 09:30:00:000000 Book 100 AAA\n2015/01/01 09:30:00:000000 Book 100 AAA')
                        result=AuquanDataSource.emitInstrumentUpdates(auqundatasource)
                        l=[]
                        count =0
                        for i in list(result):
                                l.append(i[0])
                                count+=1
                                assert isinstance(i[1][0], FutureInstrumentUpdate)
                        assert l == results["emitInstrumentUpdates"]
                        assert count ==3
                        shutil.rmtree(parameters["cachedFolderName"])
                instrumentsfromfile=InstrumentsFromFile(parameters["fileNameforinstrumentsfromfile"],
                                                        parameters["instrumentIdforinstrumentsfromfile"],
                                                        parameters["endDate"])
                linelist=parameters["line"].split("\n")
                currentBookDatalist=[]
                count=0
                for i in linelist:
                        isinstance (instrumentsfromfile.processLine(parameters["line"]), FutureInstrumentUpdate)
                        count+=1
                        currentBookDatalist.append(instrumentsfromfile.currentBookData)
                assert count==results["countforprocessLine"]
                assert currentBookDatalist == results["currentBookDatalist"]
                os.makedirs(os.path.dirname(parameters["fileNameforinstrumentsfromfile"]), exist_ok=True)
                with open(parameters["fileNameforinstrumentsfromfile"], 'w') as f:
                        f.write(parameters["line"])
                resultprocesslinesfrominstruments=InstrumentsFromFile.processLinesIntoInstruments(instrumentsfromfile)
                count=0
                for i in resultprocesslinesfrominstruments:
                        isinstance(i,FutureInstrumentUpdate)
                        count+=1
                assert count==results["countforprocessLinesIntoInstruments"]
                shutil.rmtree(parameters["cachedFolderName"])
