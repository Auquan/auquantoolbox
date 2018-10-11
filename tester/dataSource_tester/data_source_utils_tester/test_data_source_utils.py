import os, sys,shutil,pytest
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.dataSource.data_source_utils import *
from backtester.dataSource.yahoo_data_source import *
from backtester.instrumentUpdates import *
from backtester.constants import *
from data_data_source_utils import *

@pytest.fixture
def mock_stockinstrumentupdates():
    return Mock(spec=StockInstrumentUpdate)

def test_data_source_utils(mock_stockinstrumentupdates):
    for i in range(0,6):
        data = data_data_source_utils(i)
        parameters=data["parameters"]
        results=data["results"]
        dataSet=data["dataSet"]
        os.makedirs(os.path.dirname(parameters["fileName"]), exist_ok=True)
        if i==0 or i==1:
            resultgetCookieForYahoo=getCookieForYahoo(parameters["instrumentId"])
            # TODO: find a way to check the cookie and crumb
            if i==1:
                resultgetCookieForYahoo==(None,None)
            assert downloadFileFromYahoo(parameters["startDate"],parameters["endDate"],parameters["instrumentId"],parameters["fileName"],parameters["event"])==results["downloadFileFromYahoo"]
            #assert os.path.isfile(parameters["fileName"])
            if os.path.isfile(parameters["fileName"]):
                with open (parameters["fileName"],'r') as f:
                    listLine=[]
                    for line in f:
                        listLine.append(line)
                    assert listLine==dataSet["str"]
            if i==0:
                listMock=[mock_stockinstrumentupdates,mock_stockinstrumentupdates,mock_stockinstrumentupdates,mock_stockinstrumentupdates]
                mock_stockinstrumentupdates.getTimeOfUpdate.side_effect=parameters["datelist"]
                mock_stockinstrumentupdates.getStockInstrumentId.side_effect=parameters["InstrumentIdlist"]
                mock_stockinstrumentupdates.getTypeOfInstrument.side_effect=parameters["InstrumentTypelist"]
                result_timeUpdates,result_groupedInstruments=groupAndSortByTimeUpdates(listMock)
                assert result_timeUpdates==results["timeUpdates"]
                listtimeUpdates=[]
                listStockInstrumentId=[]
                listTypeOfInstrument=[]
                for inst in result_groupedInstruments:
                    assert isinstance ( inst[1][0] , StockInstrumentUpdate)
                    listStockInstrumentId.append(inst[1][0].getStockInstrumentId())
                    listTypeOfInstrument.append(inst[1][0].getTypeOfInstrument())
                    listtimeUpdates.append(inst[0])
                assert listtimeUpdates==results["timeUpdates"]
                assert listStockInstrumentId==parameters["InstrumentIdlist"]
                assert listTypeOfInstrument==parameters["InstrumentTypelist"]
                #using result_groupedInstruments from previous function
                assert getAllTimeStamps(result_groupedInstruments)==results["timeUpdates"]
############ creating YahooStockDataSource to test getMultipliers
            if i in range (2,6) :
                yds = YahooStockDataSource(cachedFolderName=parameters["folderName"],
                                           dataSetId=parameters["dataSetId"],
                                           instrumentIds=parameters["instrumentIds"],
                                           startDateStr=parameters["startDateStr"],
                                           endDateStr=parameters["endDateStr"],
                                           event=parameters["event"],
                                           liveUpdates=parameters["liveUpdates"])
################ copying from online data and testing
                if i==2:
                    resultdownloadFileFromYahoo=downloadFileFromYahoo(parameters["startDate"],parameters["endDate"],
                                                                      parameters["instrumentId"],parameters["fileName"],
                                                                      parameters["event"])
                    dfmultiplier,dftemp=getMultipliers(yds,parameters["instrumentId"],parameters["fileName"],parameters["downloadId"])
                    dfmultiplier=dfmultiplier.round(5)
                    dftemp=dftemp.round(5)
#################### checking for random dates and testing, as size is too big
                    listtemp=[dftemp.iloc[-3].tolist(),dftemp.iloc[-100].tolist(),dftemp.iloc[-50].tolist(),dftemp.iloc[-120].tolist(),dftemp.iloc[-140].tolist(),dftemp.iloc[-25].tolist()]
                    assert listtemp==results["listtemp"]
                    listmul=[dfmultiplier[0][10],dfmultiplier[1][10],dfmultiplier[0][25],dfmultiplier[1][25],dfmultiplier[0][27],dfmultiplier[1][27],dfmultiplier[0][50],dfmultiplier[1][50],dfmultiplier[0][100],dfmultiplier[1][100]]
                    assert listmul==results["listmul"]
                if i==3:
#################### getMultipliers returns None as split and div files are not present
                    resultdownloadFileFromYahoo=downloadFileFromYahoo(parameters["startDate"],parameters["endDate"],
                                                                      parameters["instrumentId"],parameters["fileName"],
                                                                      parameters["event"])
                    assert getMultipliers(yds,parameters["instrumentId"],parameters["fileName"],parameters["downloadId"])==None
                if i==4 or i==5:
#################### creating sample data and testing for it
                    os.makedirs(os.path.dirname(parameters["divfileName"]), exist_ok=True)
                    os.makedirs(os.path.dirname(parameters["splitfileName"]), exist_ok=True)
                    with open(parameters["divfileName"], 'w') as f:
                        f.write(dataSet["divData"])
                    with open(parameters["splitfileName"], 'w') as f:
                        f.write(dataSet["splitData"])
                    with open(parameters["fileName"], 'w') as f:
                        f.write(dataSet["fileData"])
                    dfmultiplier,dftemp=getMultipliers(yds,parameters["instrumentId"],parameters["fileName"],parameters["downloadId"])
                    listTemp=[]
                    for ele in dftemp:
                        listTemp.append(dftemp[ele].tolist())
                    assert listTemp==results["listTemp"]
                    listMultiplier=[]
                    for ele in dfmultiplier:
                        listMultiplier.append(dfmultiplier[ele].tolist())
                    assert listMultiplier==results["listMultiplier"]
        shutil.rmtree(parameters["folderName"])
