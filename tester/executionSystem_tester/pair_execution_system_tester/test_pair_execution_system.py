import os,sys,pytest,pandas as pd,numpy as np
from datetime import datetime
from unittest.mock import Mock, MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.executionSystem.base_execution_system import *
from backtester.executionSystem.pair_execution_system import *
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.lookback_data import *
from data_pair_execution_system import *

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
def mock_lookbackdata():
    return Mock(spec=LookbackData)

def test_pair_execution_system(mock_instrumentmanager, mock_instrumentlookbackdata,mock_lookbackdata):
    for i in range(0,4):
        data = data_pair_execution_system(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        pairexecutionsystem=PairExecutionSystem(parameters["pair"],parameters["pairRatio"],parameters["pairEnter_threshold"],
                                                parameters["pairExit_threshold"],parameters["pairLongLimit"],
                                                parameters["pairShortLimit"],parameters["pairCapitalUsageLimit"],
                                                parameters["pairLotSize"],parameters["price"])
######## mocking the functions
        def sideeffect(value):
            if (value=='close'):
                return dataSet["price"]
            else:
                return dataSet[value]
        dict={'prediction':dataSet["prediction"]}
        mock_instrumentmanager.getLookbackMarketFeatures.return_value = mock_lookbackdata
        mock_lookbackdata.getData.return_value=dict
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
######## testing for error producing data
        if i==0 or i==1:
            assert PairExecutionSystem.getExecutions(pairexecutionsystem,parameters["time"],mock_instrumentmanager,parameters["capital"])==results["getExecutions"]
######## testing for sample data
        else:
            resultgetexecutions=PairExecutionSystem.getExecutions(pairexecutionsystem,parameters["time"],mock_instrumentmanager,parameters["capital"])
            count=0
            listExecutionType=[]
            listVolume=[]
            listInstrumentId=[]
            listTimeOfExecution=[]
            for x in resultgetexecutions:
                assert isinstance(x,InstrumentExection)
                listExecutionType.append(x.getExecutionType())
                listVolume.append(x.getVolume())
                listInstrumentId.append(x.getInstrumentId())
                listTimeOfExecution.append(x.getTimeOfExecution())
                count+=1
            assert count == results["count"]
            assert listVolume==results["listVolume"]
            assert listInstrumentId==results["listInstrumentId"]
            assert listExecutionType==results["listExecutionType"]
            assert listTimeOfExecution==results["listTimeOfExecution"]
