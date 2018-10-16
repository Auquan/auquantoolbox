import os,sys,pytest,pandas as pd,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
from collections import OrderedDict
sys.path.append(os.path.abspath(''))
from backtester.executionSystem.QQ_execution_system import QQExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_QQ_execution_system import *

#mocking InstrumentManager
@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
#mocking InstrumentsLookbackData
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_QQ_execution_system(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,4):
        data = data_QQ_execution_system(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        qqexecutionsystem=QQExecutionSystem(parameters["basisEnter_threshold"],parameters["basisExit_threshold"],
                                            parameters["basisLongLimit"],parameters["basisShortLimit"],
                                            parameters["basisCapitalUsageLimit"], parameters["basisLotSize"],
                                            parameters["basisLimitType"],parameters["basis_thresholdParam"],
                                            parameters["price"],parameters["feeDict"])
######## mocking for each function being used
        def sideeffect(value):
            if (value=='close'):
                return dataSet["price"]
            else:
                return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
######## testing for error producing data
        if i==0 or i==1:
            assert QQExecutionSystem.getDeviationFromPrediction(qqexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["getDeviationFromPrediction"]
            assert QQExecutionSystem.getBuySell(qqexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["getBuySell"]
            assert QQExecutionSystem.enterCondition(qqexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["enterCondition"]
            assert QQExecutionSystem.exitCondition(qqexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["exitCondition"]
######## testing for sample data
        else:
            assert QQExecutionSystem.getDeviationFromPrediction(qqexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).round(2).equals(results["getDeviationFromPrediction"])
            assert QQExecutionSystem.getBuySell(qqexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["getBuySell"])
            assert QQExecutionSystem.enterCondition(qqexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["enterCondition"])
            assert QQExecutionSystem.exitCondition(qqexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["exitCondition"])
