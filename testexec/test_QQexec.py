from backtester.executionSystem.QQ_execution_system import QQExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import pandas as pd
import pytest
from initialize import Initialize
import numpy as np

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
        return Mock(spec=InstrumentsLookbackData)

def test_QQexec(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(1,6):
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                results=dataSet["results"]
                def sideeffect(value):
                        if (value=='close'):
                                return data["price"]
                        if (value=='sdev'):
                                return data["sdev"]
                        if (value=='position'):
                                return data["position"]
                qqexecutionsystem=QQExecutionSystem(parameters["basisEnter_thresholdforQQExec"],parameters["basisExit_thresholdforQQExec"],parameters["basisLongLimit"],
                                                    parameters["basisShortLimit"],parameters["basisCapitalUsageLimit"], parameters["basisLotSize"], parameters["basisLimitType"],
                                                    parameters["basis_thresholdParam"], parameters["priceforSimpleExec"],parameters["feeDictforQQExec"])
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultgetdeviationfromprediction=QQExecutionSystem.getDeviationFromPrediction(qqexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert list(np.around(np.array(resultgetdeviationfromprediction.tolist()),2)) == results["getDeviationFromPredictionforQQExec"]
                resultgetbuysell=QQExecutionSystem.getBuySell(qqexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultgetbuysell.tolist() == results["getBuySellforQQExec"]
                resultentercondition=QQExecutionSystem.enterCondition(qqexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultentercondition.tolist() == results["enterConditionforQQExec"]
                resultexitcondition=QQExecutionSystem.exitCondition(qqexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultexitcondition.tolist() == results["exitConditionforQQExec"]
