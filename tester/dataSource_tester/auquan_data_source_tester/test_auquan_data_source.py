import os,sys,shutil,pytest
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.auquan_data_source import *
from backtester.instrumentUpdates import *
from backtester.logger import *
from data_auquan_data_source import *

def test_auquan_data_source():
    for i in range(0,5):
        data= data_auquan_data_source(i)
        parameters=data["parameters"]
        results=data["results"]
        if i==0 or i==1:
            assert checkDate(parameters["lineItem"]) == results["checkDate"]
            assert checkTimestamp(parameters["lineItem"]) == results["checkTimestamp"]
        assert validateLineItem(parameters["lineItems"]) ==results["validateLineItem"]
        assert parseBookDataOptionLine(parameters["lineItems"]) == results["parseBookDataOptionLine"]
        assert get_exp_date(parameters["trade_date"]) == results["get_exp_date"]
######## testing for InstrumentsFromFile Class
        if i in range(0,3):
            instrumentsfromfile=InstrumentsFromFile(parameters["fileName"],parameters["instrumentId"],parameters["expiryTime"])
            linelist=parameters["line"].split("\n")
            currentBookDatalist=[]
            count=0
            for c in linelist:
                inst=instrumentsfromfile.processLine(parameters["line"])
                if i==0:
                    assert inst==None
                if i==1:
                    #defining inst again because for first run inst=None
                    inst=instrumentsfromfile.processLine(parameters["line"])
                    assert isinstance (inst, FutureInstrumentUpdate)
                    assert inst.getFutureInstrumentId()=="GOOG"
                    assert inst.getTypeOfInstrument()=="future"
                    assert inst.getExpiryTime()==datetime(2018, 1, 9, 0, 0)
                    assert inst.getUnderlyingInstrumentId()=="NA"
                count+=1
                if i==2:
                    assert instrumentsfromfile.currentBookData == results["currentBookData"]
            assert count==results["countforprocessLine"]
            os.makedirs(os.path.dirname(parameters["fileName"]),exist_ok=True)
            with open(parameters["fileName"], 'w') as f:
                f.write(parameters["line"])
            resultprocesslinesfrominstruments=InstrumentsFromFile.processLinesIntoInstruments(instrumentsfromfile)
            count=0
            for ele in resultprocesslinesfrominstruments:
                if i==1:
                    assert isinstance(ele,FutureInstrumentUpdate)
                    assert ele.getFutureInstrumentId()=="GOOG"
                    assert ele.getTypeOfInstrument()=="future"
                    assert ele.getExpiryTime()==datetime(2018, 1, 9, 0, 0)
                    assert ele.getUnderlyingInstrumentId()=="NA"
                count+=1
            assert count==results["countforprocessLinesIntoInstruments"]
            shutil.rmtree(parameters["folderName"])
######## testing for AuquanDataSource Class
        if i==0:
            auqundatasource=AuquanDataSource(parameters["folderName"],parameters["instrumentIdsByType"],
                                             parameters["startDateStr"],parameters["endDateStr"],
                                             parameters["liveUpdates"])
            assert AuquanDataSource.getFileName(auqundatasource,parameters["instrumentType"],parameters["instrumentId"],parameters["date"]) == results["getFileName"]
            os.makedirs(os.path.dirname('Folder1/b/BBA/BBA_20180102.txt'), exist_ok=True)
            os.makedirs(os.path.dirname('Folder1/b/BPM/BPM_20180102.txt'), exist_ok=True)
            with open('Folder1/b/BBA/BBA_20180102.txt', 'w') as f:
                f.write('2017/01/01 09:30:00:000000 Book 100 AAA\n2018/01/01 09:30:00:000000 Book 100 AAA\n2019/01/01 09:30:00:000000 Book 100 AAA')
            with open('Folder1/b/BPM/BPM_20180102.txt', 'w') as f:
                f.write('2016/01/01 09:30:00:000000 Book 100 AAA\n2015/01/01 09:30:00:000000 Book 100 AAA')
            result=AuquanDataSource.emitInstrumentUpdates(auqundatasource)
            listDates=[]
            listFutureInstrumentId=[]
            listTypeOfInstrument=[]
            listExpiryTime=[]
            listUnderlyingInstrumentId=[]
            count=0
            for ele in list(result):
                assert isinstance(ele[1][0], FutureInstrumentUpdate)
                listDates.append(ele[0])
                listFutureInstrumentId.append(ele[1][0].getFutureInstrumentId())
                listTypeOfInstrument.append(ele[1][0].getTypeOfInstrument())
                listExpiryTime.append(ele[1][0].getExpiryTime())
                listUnderlyingInstrumentId.append(ele[1][0].getUnderlyingInstrumentId())
                count+=1
            assert listDates == results["emitInstrumentUpdates"]
            assert count == results["countforemitInstrumentUpdates"]
            assert listFutureInstrumentId==results["listFutureInstrumentId"]
            assert listTypeOfInstrument==results["listTypeOfInstrument"]
            assert listExpiryTime==results["listExpiryTime"]
            assert listUnderlyingInstrumentId==results["listUnderlyingInstrumentId"]
            shutil.rmtree(parameters["folderName"])
        if i==1:
            auqundatasource2=AuquanDataSource(parameters["folderName"],parameters["instrumentIdsByType"],
                                             parameters["startDateStr"],parameters["endDateStr"],
                                             parameters["liveUpdates"])
            assert AuquanDataSource.getFileName(auqundatasource2,parameters["instrumentType"],parameters["instrumentId"],parameters["date"]) == results["getFileName"]
            os.makedirs(os.path.dirname('Folder1/b/BBA/BBA_20180102.txt'), exist_ok=True)
            os.makedirs(os.path.dirname('Folder1/b/BPM/BPM_20180102.txt'), exist_ok=True)
            with open('Folder1/b/BBA/BBA_20180102.txt', 'w') as f:
                f.write('')
            with open('Folder1/b/BPM/BPM_20180102.txt', 'w') as f:
                f.write('')
            result=AuquanDataSource.emitInstrumentUpdates(auqundatasource2)
            listDates=[]
            listFutureInstrumentId=[]
            listTypeOfInstrument=[]
            listExpiryTime=[]
            listUnderlyingInstrumentId=[]
            count=0
            for ele in list(result):
                assert isinstance(ele[1][0], FutureInstrumentUpdate)
                listDates.append(ele[0])
                listFutureInstrumentId.append(ele[1][0].getFutureInstrumentId())
                listTypeOfInstrument.append(ele[1][0].getTypeOfInstrument())
                listExpiryTime.append(ele[1][0].getExpiryTime())
                listUnderlyingInstrumentId.append(ele[1][0].getUnderlyingInstrumentId())
                count+=1
            assert listDates == results["emitInstrumentUpdates"]
            assert count == results["countforemitInstrumentUpdates"]
            assert listFutureInstrumentId==results["listFutureInstrumentId"]
            assert listTypeOfInstrument==results["listTypeOfInstrument"]
            assert listExpiryTime==results["listExpiryTime"]
            assert listUnderlyingInstrumentId==results["listUnderlyingInstrumentId"]
            shutil.rmtree(parameters["folderName"])
