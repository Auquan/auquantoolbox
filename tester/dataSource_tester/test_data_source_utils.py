import os, sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.dataSource.data_source_utils import *
from backtester.dataSource.yahoo_data_source import *
from backtester.instrumentUpdates import *
from backtester.constants import *
from backtester.logger import *
from datetime import datetime, time, timedelta
from unittest.mock import Mock, MagicMock
import pytest
from initializeds import Initialize

@pytest.fixture
def mock_stockinstrumentupdates():
        return Mock(spec=StockInstrumentUpdate)

def test_data_source_utils(mock_stockinstrumentupdates):
        initialize=Initialize()
        for i in range(0,2):
                dataSet = initialize.getDataSet(i)
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                data=dataSet["dataSet"]
                resultgetCookieForYahoo=getCookieForYahoo(parameters["instrumentId"])
                resultdownloadFileFromYahoo=downloadFileFromYahoo(parameters["startDate"],parameters["endDate"],
                                                                  parameters["instrumentId"],parameters["fileName"],
                                                                  parameters["event"])
                assert os.path.isfile(parameters["fileName"])
                if i==0:
                        with open (parameters["fileName"],'r') as f:
                                content=f.read()
                                assert content==data["str"]
                os.remove(parameters["fileName"])
                list=[mock_stockinstrumentupdates,mock_stockinstrumentupdates,mock_stockinstrumentupdates,mock_stockinstrumentupdates]
                mock_stockinstrumentupdates.getTimeOfUpdate.side_effect=parameters["datelist"]
                resultgroupAndSortByTimeUpdatestimeUpdates,resultgroupAndSortByTimeUpdatesgroupedInstruments=groupAndSortByTimeUpdates(list)
                assert resultgroupAndSortByTimeUpdatestimeUpdates==results["timeUpdates"]
                list=[]
                for inst in resultgroupAndSortByTimeUpdatesgroupedInstruments:
                        assert isinstance ( inst[1][0] , StockInstrumentUpdate)
                        list.append(inst[0])
                assert list==results["timeUpdates"]
                resultgetAllTimeStamps=getAllTimeStamps(resultgroupAndSortByTimeUpdatesgroupedInstruments)
                assert resultgetAllTimeStamps==results["timeUpdates"]
                if i==0:
                        instrumentIds = ['IBM', 'AAPL']
                        for c in range(0,2):
                            if c==0:
                                startDateStr = '2014/05/01'
                                endDateStr = '2014/11/30'
                            if c==1:
                                startDateStr = '2014/01/01'
                                endDateStr = '2014/01/30'
                            yds = YahooStockDataSource(cachedFolderName='Folder1/',
                                                             dataSetId="QQ3Data",
                                                     instrumentIds=instrumentIds,
                                                     startDateStr=startDateStr,
                                                     endDateStr=endDateStr,
                                                     event='history',
                                                     liveUpdates=True)
                            stdate=datetime.strptime(startDateStr,"%Y/%m/%d")
                            endate=datetime.strptime(endDateStr,"%Y/%m/%d")
                            resultdownloadFileFromYahoo=downloadFileFromYahoo(stdate,endate,
                                                                              parameters["instrumentId"],parameters["fileName"],
                                                                              parameters["event"])
                            if c==0:
                                dfmultiplier,dftemp=getMultipliers(yds,"AAPL",parameters["fileName"],".SN")
                                dfmultiplier=dfmultiplier.round(5)
                                dftemp=dftemp.round(5)
                                listtemp=[dftemp.iloc[-3].tolist(),dftemp.iloc[-100].tolist(),dftemp.iloc[-50].tolist(),dftemp.iloc[-120].tolist(),dftemp.iloc[-140].tolist(),dftemp.iloc[-25].tolist()]
                                assert listtemp==results["listtemp"]
                                listmul=[dfmultiplier[0][10],dfmultiplier[1][10],dfmultiplier[0][25],dfmultiplier[1][25],dfmultiplier[0][27],dfmultiplier[1][27],dfmultiplier[0][50],dfmultiplier[1][50],dfmultiplier[0][100],dfmultiplier[1][100]]
                                assert listmul==results["listmul"]
                            if c==1:
                                assert getMultipliers(yds,"AAPL",parameters["fileName"],".SN")==None
                            os.remove(parameters["fileName"])
                            shutil.rmtree(parameters["cachedFolderName"])
