import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.executionSystem.simple_execution_system_fairvalue import SimpleExecutionSystemWithFairValue
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import pandas as pd
import pytest
from initializeexec import Initialize
import numpy as np

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
        return Mock(spec=InstrumentsLookbackData)

def test_simple_execution_system_fairvalue(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(1,6):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                dict=dataSet["dict"]
                def sideeffect(value):
                        if (value=='close'):
                                return data["price"]
                simpleexecutionsystemwithfairvalue=SimpleExecutionSystemWithFairValue(parameters["enter_threshold_deviation"],parameters["exit_threshold_deviation"],parameters["longLimit"],
                                                                                      parameters["shortLimit"],parameters["capitalUsageLimit"], parameters["enterlotSize"], parameters["exitlotSize"],
                                                                                      parameters["limitType"], parameters["priceforSimpleExec"])
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultgetdeviationfromprediction=SimpleExecutionSystemWithFairValue.getDeviationFromPrediction(simpleexecutionsystemwithfairvalue,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert list(np.around(np.array(resultgetdeviationfromprediction.tolist()),2)) == results["getDeviationFromPredictionforSimpleFairValueExec"]
                resultgetbuysell=SimpleExecutionSystemWithFairValue.getBuySell(simpleexecutionsystemwithfairvalue,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultgetbuysell.tolist() == results["getBuySellforforSimpleFairValueExec"]
                resultentercondition=SimpleExecutionSystemWithFairValue.enterCondition(simpleexecutionsystemwithfairvalue,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultentercondition.tolist() == results["enterConditionforSimpleFairValueExec"]
                resultexitcondition=SimpleExecutionSystemWithFairValue.exitCondition(simpleexecutionsystemwithfairvalue,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultexitcondition.tolist() == results["exitConditionforSimpleFairValueExec"]
                resulthackcondition=SimpleExecutionSystemWithFairValue.hackCondition(simpleexecutionsystemwithfairvalue,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resulthackcondition.tolist() == results["hackConditionforSimpleFairValueExec"]
