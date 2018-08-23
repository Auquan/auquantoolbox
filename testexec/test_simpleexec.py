from backtester.executionSystem.base_execution_system import *
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import *
from unittest.mock import Mock, MagicMock
import pandas as pd
import pytest
from initialize import Initialize

#mocking InstrumentManager
@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
#mocking InstrumentsLookbackData
@pytest.fixture
def mock_instrumentlookbackdata():
        return Mock(spec=InstrumentsLookbackData)
#mocking Instrument
@pytest.fixture
def mock_instrument():
        return Mock(spec=Instrument)

def test_QQexec(mock_instrumentmanager, mock_instrumentlookbackdata,mock_instrument):
        initialize = Initialize()
        for i in range(0,6):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                dict=dataSet["dict"]
                def sideeffect(value):
                        if (value=='close'):
                                return data["price"]
                        if (value=='position'):
                                return data["position"]
                        if (value=='prediction'):
                                return data["prediction"]
                dictinstruments={'a':mock_instrument,
                                 'b':mock_instrument,
                                 'c':mock_instrument,
                                 'd':mock_instrument}
                d={'a':1,'b':2,'c':0,'d':4,'e':0,'f':3}
                simpleexecutionsystem=SimpleExecutionSystem(parameters["enter_threshold"],parameters["exit_threshold"],
                                                            parameters["longLimit"],parameters["shortLimit"],
                                                            parameters["capitalUsageLimit"],parameters["enterlotSize"],
                                                            parameters["exitlotSize"],parameters["limitType"],parameters["priceforSimpleExec"])
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dictinstruments
                mock_instrument.getCurrentPosition.side_effect=[2,0,1,3]
                if i==0:
                        SimpleExecutionSystem.getPriceSeries(simpleexecutionsystem,mock_instrumentmanager)
                else:
                        resultgetpriceseries=SimpleExecutionSystem.getPriceSeries(simpleexecutionsystem,mock_instrumentmanager)
                        assert list(resultgetpriceseries) == results["getPriceSeriesforSimpleExec"]
                        resultgetlonglimit=SimpleExecutionSystem.getLongLimit(simpleexecutionsystem,dict,resultgetpriceseries)
                        assert resultgetlonglimit.values.T.tolist() == results["getLongLimitforSimpleExec"]
                        resultgetshortlimit=SimpleExecutionSystem.getShortLimit(simpleexecutionsystem,dict,resultgetpriceseries)
                        assert resultgetshortlimit.values.T.tolist() == results["getShortLimitforSimpleExec"]
                        resultgetenterlotsize=SimpleExecutionSystem.getEnterLotSize(simpleexecutionsystem,dict,resultgetpriceseries)
                        assert resultgetenterlotsize.values.T.tolist() == results["getEnterLotSizeforSimpleExec"]
                        resultgetexitlotsize=SimpleExecutionSystem.getExitLotSize(simpleexecutionsystem,dict,resultgetpriceseries)
                        assert resultgetexitlotsize.values.T.tolist() == results["getExitLotSizeforSimpleExec"]
                        resultconvertLimit=SimpleExecutionSystem.convertLimit(simpleexecutionsystem,data["df"],resultgetpriceseries)
                        assert resultconvertLimit.values.T.tolist() == results["convertLimitforSimpleExec"]
                        s=pd.Series(d)
                        resultgetinstrumentexecutionsfromexecutions=SimpleExecutionSystem.getInstrumentExecutionsFromExecutions(simpleexecutionsystem,"01/01/2010",s)
                        count=0
                        for x in resultgetinstrumentexecutionsfromexecutions:
                                assert isinstance(x,InstrumentExection)
                                count+=1
                        assert count==4
                        resultexitposition=SimpleExecutionSystem.exitPosition(simpleexecutionsystem,"01/01/2010",mock_instrumentmanager,data["prediction"].iloc[-1],parameters["closeAllPositions"])
                        assert resultexitposition.tolist() == results["exitPositionforSimpleExec"]
                        resultenterposition=SimpleExecutionSystem.enterPosition(simpleexecutionsystem,"01/01/2010",mock_instrumentmanager,data["prediction"].iloc[-1],parameters["capital"])
                        assert resultenterposition.tolist() == results["enterPositionforSimpleExec"]
                        resultgetbuysell=SimpleExecutionSystem.getBuySell(simpleexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                        assert resultgetbuysell.tolist() == results["getBuySellforSimpleExec"]
                        resultentercondition=SimpleExecutionSystem.enterCondition(simpleexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                        assert resultentercondition.tolist() == results["enterConditionforSimpleExec"]
                        resultatpositionlimit=SimpleExecutionSystem.atPositionLimit(simpleexecutionsystem,parameters["capital"],data["position"],resultgetpriceseries)
                        assert resultatpositionlimit.tolist() == results["atPositionLimitforSimpleExec"]
                        resultexitcondition=SimpleExecutionSystem.exitCondition(simpleexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                        assert resultexitcondition.tolist() == results["exitConditionforSimpleExec"]
                        resulthackcondition=SimpleExecutionSystem.hackCondition(simpleexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                        assert resulthackcondition.tolist() == results["hackConditionforSimpleExec"]
                        resultgetexecutionsatclose=SimpleExecutionSystem.getExecutionsAtClose(simpleexecutionsystem,"01/01/2010",mock_instrumentmanager)
                        count=0
                        for x in resultgetexecutionsatclose:
                                assert isinstance(x,InstrumentExection)
                                count+=1
                        assert count==3
                        resultgetexecutions=SimpleExecutionSystem.getExecutions(simpleexecutionsystem,"01/01/2010",mock_instrumentmanager,parameters["capital"])
                        count=0
                        for x in resultgetexecutions:
                                assert isinstance(x,InstrumentExection)
                                count+=1
                        assert count==parameters["count"]
