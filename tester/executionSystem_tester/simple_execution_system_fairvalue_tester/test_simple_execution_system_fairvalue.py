import os,sys,pytest,pandas as pd,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.executionSystem.simple_execution_system_fairvalue import SimpleExecutionSystemWithFairValue
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_simple_execution_system_fairvalue import *

#mocking InstrumentManager
@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
#mocking InstrumentsLookbackData
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_simple_execution_system_fairvalue(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,4):
        data = data_simple_execution_system_fairvalue(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        simpleexecutionsystemwithfairvalue=SimpleExecutionSystemWithFairValue(parameters["enter_threshold_deviation"],parameters["exit_threshold_deviation"],
                                                                              parameters["longLimit"],parameters["shortLimit"],parameters["capitalUsageLimit"],
                                                                              parameters["enterlotSize"],parameters["exitlotSize"],parameters["limitType"],
                                                                              parameters["price"])
######## mocking for every function
        def sideeffect(value):
            if (value=='close'):
                    return dataSet["price"]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
######## testing for error causing data
        if i==0 or i==1:
            with pytest.raises(Exception) as e_info:
                assert SimpleExecutionSystemWithFairValue.getDeviationFromPrediction(simpleexecutionsystemwithfairvalue,pd.DataFrame(),mock_instrumentmanager)==results["getDeviationFromPrediction"]
                assert SimpleExecutionSystemWithFairValue.getBuySell(simpleexecutionsystemwithfairvalue,pd.DataFrame(),mock_instrumentmanager)==results["getBuySell"]
                assert SimpleExecutionSystemWithFairValue.enterCondition(simpleexecutionsystemwithfairvalue,pd.DataFrame(),mock_instrumentmanager)==results["enterCondition"]
                assert SimpleExecutionSystemWithFairValue.exitCondition(simpleexecutionsystemwithfairvalue,pd.DataFrame(),mock_instrumentmanager)==results["exitCondition"]
                assert SimpleExecutionSystemWithFairValue.hackCondition(simpleexecutionsystemwithfairvalue,pd.DataFrame(),mock_instrumentmanager).equals(results["hackCondition"])
######## testing for sample data
        else:
            assert SimpleExecutionSystemWithFairValue.getDeviationFromPrediction(simpleexecutionsystemwithfairvalue,dataSet["prediction"].iloc[-1],mock_instrumentmanager).round(2).equals(results["getDeviationFromPrediction"])
            assert SimpleExecutionSystemWithFairValue.getBuySell(simpleexecutionsystemwithfairvalue,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["getBuySell"])
            assert SimpleExecutionSystemWithFairValue.enterCondition(simpleexecutionsystemwithfairvalue,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["enterCondition"])
            assert SimpleExecutionSystemWithFairValue.exitCondition(simpleexecutionsystemwithfairvalue,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["exitCondition"])
            assert SimpleExecutionSystemWithFairValue.hackCondition(simpleexecutionsystemwithfairvalue,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["hackCondition"])
