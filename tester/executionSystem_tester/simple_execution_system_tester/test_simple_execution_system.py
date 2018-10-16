import os,sys,pytest,pandas as pd
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.executionSystem.base_execution_system import *
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import *
from data_simple_execution_system import *

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

def test_simple_execution_system(mock_instrumentmanager, mock_instrumentlookbackdata,mock_instrument):
    for i in range(0,10):
        data = data_simple_execution_system(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        simpleexecutionsystem=SimpleExecutionSystem(parameters["enter_threshold"],parameters["exit_threshold"],
                                                    parameters["longLimit"],parameters["shortLimit"],
                                                    parameters["capitalUsageLimit"],parameters["enterlotSize"],
                                                    parameters["exitlotSize"],parameters["limitType"],
                                                    parameters["price"])
######## mocking for functions being used
        def sideeffect(value):
            if (value=='close'):
                return dataSet["price"]
            else:
                return dataSet[value]
        dictinstruments={'a':mock_instrument,
                         'b':mock_instrument,
                         'c':mock_instrument,
                         'd':mock_instrument}
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
######## testing for error causing data
        if i==0 or i==1:
            assert SimpleExecutionSystem.getPriceSeries(simpleexecutionsystem,mock_instrumentmanager)==results["getPriceSeries"]
            assert SimpleExecutionSystem.getLongLimit(simpleexecutionsystem,dataSet["dict"],pd.Series()).equals(results["getLongLimit"])
            assert SimpleExecutionSystem.getShortLimit(simpleexecutionsystem,dataSet["dict"],pd.Series()).equals(results["getShortLimit"])
            assert SimpleExecutionSystem.getEnterLotSize(simpleexecutionsystem,dataSet["dict"],pd.Series()).equals(results["getEnterLotSize"])
            assert SimpleExecutionSystem.getExitLotSize(simpleexecutionsystem,dataSet["dict"],pd.Series()).equals(results["getExitLotSize"])
            assert SimpleExecutionSystem.convertLimit(simpleexecutionsystem,parameters["convertLimitdf"],pd.Series()).equals(results["convertLimit"])
######## testing for different sample data
        else:
            assert SimpleExecutionSystem.getPriceSeries(simpleexecutionsystem,mock_instrumentmanager).round(2).equals(results["getPriceSeries"])
            assert SimpleExecutionSystem.getLongLimit(simpleexecutionsystem,dataSet["dict"],parameters["priceSeries"]).equals(results["getLongLimit"])
            assert SimpleExecutionSystem.getShortLimit(simpleexecutionsystem,dataSet["dict"],parameters["priceSeries"]).equals(results["getShortLimit"])
            assert SimpleExecutionSystem.getEnterLotSize(simpleexecutionsystem,dataSet["dict"],parameters["priceSeries"]).equals(results["getEnterLotSize"])
            assert SimpleExecutionSystem.getExitLotSize(simpleexecutionsystem,dataSet["dict"],parameters["priceSeries"]).equals(results["getExitLotSize"])
            assert SimpleExecutionSystem.convertLimit(simpleexecutionsystem,parameters["convertLimitdf"],parameters["priceSeries"]).equals(results["convertLimit"])
######## testing for error causing data
        if i==0 or i==1:
            assert SimpleExecutionSystem.getInstrumentExecutionsFromExecutions(simpleexecutionsystem,parameters["time"],parameters["executions"])==results["getInstrumentExecutionsFromExecutions"]
            assert SimpleExecutionSystem.getExecutions(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,parameters["capital"])==results["getExecutions"]
            dictinstruments={}
            mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dictinstruments
            assert SimpleExecutionSystem.getExecutionsAtClose(simpleexecutionsystem,parameters["time"],mock_instrumentmanager)==results["getExecutionsAtClose"]
######## testing for different sample data
        if i==2 or i==4:
            resultgetinstrumentexecutionsfromexecutions=SimpleExecutionSystem.getInstrumentExecutionsFromExecutions(simpleexecutionsystem,parameters["time"],parameters["executions"])
            count=0
            listTimeOfExecution=[]
            listInstrumentId=[]
            listVolume=[]
            listExecutionType=[]
            for x in resultgetinstrumentexecutionsfromexecutions:
                assert isinstance(x,InstrumentExection)
                listTimeOfExecution.append(x.getTimeOfExecution())
                listInstrumentId.append(x.getInstrumentId())
                listVolume.append(x.getVolume())
                listExecutionType.append(x.getExecutionType())
                count+=1
            assert count==results["countforgetinstrumentexecutionsfromexecutions"]
            resultgetexecutions=SimpleExecutionSystem.getExecutions(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,parameters["capital"])
            count=0
            for x in resultgetexecutions:
                assert isinstance(x,InstrumentExection)
                listTimeOfExecution.append(x.getTimeOfExecution())
                listInstrumentId.append(x.getInstrumentId())
                listVolume.append(x.getVolume())
                listExecutionType.append(x.getExecutionType())
                count+=1
            assert count==results["countforgetexecutions"]
############ mocking functions
            dictinstruments={'a':mock_instrument,
                             'b':mock_instrument,
                             'c':mock_instrument,
                             'd':mock_instrument}
            mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dictinstruments
            mock_instrument.getCurrentPosition.side_effect=parameters["getCurrentPosition"]
            mock_instrument.getInstrumentId.side_effect=parameters["getInstrumentId"]
            resultgetexecutionsatclose=SimpleExecutionSystem.getExecutionsAtClose(simpleexecutionsystem,parameters["time"],mock_instrumentmanager)
            count=0
            for x in resultgetexecutionsatclose:
                assert isinstance(x,InstrumentExection)
                listTimeOfExecution.append(x.getTimeOfExecution())
                listInstrumentId.append(x.getInstrumentId())
                listVolume.append(x.getVolume())
                listExecutionType.append(x.getExecutionType())
                count+=1
            assert count==results["countforgetexecutionsatclose"]
            assert listTimeOfExecution==results["listTimeOfExecution"]
            assert listInstrumentId==results["listInstrumentId"]
            assert listVolume==results["listVolume"]
            assert listExecutionType==results["listExecutionType"]
######## testing for IndexError causing data
        if i==0:
            assert SimpleExecutionSystem.exitPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,pd.Series(),parameters["closeAllPositions"])==results["exitPosition"]
            assert SimpleExecutionSystem.enterPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,pd.Series(),parameters["capital"])==results["enterPosition"]
            assert SimpleExecutionSystem.getBuySell(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["getBuySell"])
            assert SimpleExecutionSystem.enterCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["enterCondition"])
            assert SimpleExecutionSystem.atPositionLimit(simpleexecutionsystem,parameters["capital"],dataSet["position"],parameters["priceSeries"])==results["atPositionLimit"]
            assert SimpleExecutionSystem.exitCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["exitCondition"])
            assert SimpleExecutionSystem.hackCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["hackCondition"])
######## testing for pd.core.indexing.IndexingError causing data
        if i==2:
            assert SimpleExecutionSystem.exitPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,pd.Series(),parameters["closeAllPositions"])==results["exitPosition"]
            assert SimpleExecutionSystem.enterPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,pd.Series(),parameters["capital"])==results["enterPosition"]
            assert SimpleExecutionSystem.getBuySell(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["getBuySell"])
            assert SimpleExecutionSystem.enterCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["enterCondition"])
            assert SimpleExecutionSystem.atPositionLimit(simpleexecutionsystem,parameters["capital"],dataSet["positionData"],parameters["priceSeries"]).equals(results["atPositionLimit"])
            assert SimpleExecutionSystem.exitCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["exitCondition"])
            assert SimpleExecutionSystem.hackCondition(simpleexecutionsystem,pd.Series(),mock_instrumentmanager).equals(results["hackCondition"])
######## testing for sample data
        if i==3 or i==4:
            assert SimpleExecutionSystem.exitPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,dataSet["prediction"].iloc[-1],parameters["closeAllPositions"]).equals(results["exitPosition"])
            assert SimpleExecutionSystem.enterPosition(simpleexecutionsystem,parameters["time"],mock_instrumentmanager,dataSet["prediction"].iloc[-1],parameters["capital"]).equals(results["enterPosition"])
            assert SimpleExecutionSystem.getBuySell(simpleexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["getBuySell"])
            assert SimpleExecutionSystem.enterCondition(simpleexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["enterCondition"])
            assert SimpleExecutionSystem.atPositionLimit(simpleexecutionsystem,parameters["capital"],dataSet["positionData"],parameters["priceSeries"]).equals(results["atPositionLimit"])
            assert SimpleExecutionSystem.exitCondition(simpleexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["exitCondition"])
            assert SimpleExecutionSystem.hackCondition(simpleexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["hackCondition"])
