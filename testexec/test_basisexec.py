from backtester.executionSystem.basis_execution_system import BasisExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import *
from unittest.mock import Mock, MagicMock
import time
from datetime import datetime, time, timedelta
from collections import OrderedDict
import math
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
@pytest.fixture
def mock_instrument():
        return Mock(spec=Instrument)

def test_basisexec(mock_instrumentmanager, mock_instrumentlookbackdata,mock_instrument):
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
                        if (value=='stockTopBidPrice'):
                                return data["stockTopBidPrice"]
                        if (value=='stockTopAskPrice'):
                                return data["stockTopAskPrice"]
                        if (value=='futureTopBidPrice'):
                                return data["futureTopBidPrice"]
                        if (value=='futureTopAskPrice'):
                                return data["futureTopAskPrice"]
                        if (value=='stockVWAP'):
                                return data["stockVWAP"]
                        if (value=='position'):
                                return data["position"]
                        if (value=='enter_price'):
                                return data["enter_price"]
                        if (value=='sdev'):
                                return data["sdev"]
                basisexecutionsystem=BasisExecutionSystem(parameters["basisEnter_thresholdforBasisExec"],parameters["basisExit_thresholdforBasisExec"],parameters["basisLongLimit"],
                                                          parameters["basisShortLimit"],parameters["basisCapitalUsageLimit"], parameters["basisLotSize"],
                                                          parameters["basisLimitType"], parameters["basis_thresholdParam"],parameters["priceforSimpleExec"], parameters["feeDict"],
                                                          parameters["feesRatio"], parameters["spreadLimit"],parameters["hackTime"])
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dict
                mock_instrumentmanager.getInstrument.return_value=mock_instrument
                mock_instrument.getCurrentPosition.side_effect=[2,3,0,2,0]
                resultgetdeviationfromprediction=BasisExecutionSystem.getDeviationFromPrediction(basisexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert list(np.around(np.array(resultgetdeviationfromprediction.tolist()),2)) == results["getDeviationFromPredictionforBasisExec"]
                resultgetspread=BasisExecutionSystem.getSpread(basisexecutionsystem,mock_instrumentmanager)
                assert resultgetspread.tolist() == results["getSpreadforBasisExec"]
                resultgetfees=BasisExecutionSystem.getFees(basisexecutionsystem,mock_instrumentmanager)
                assert list(np.around(np.array(resultgetfees.tolist()),10)) == results["getFeesforBasisExec"]
                resultgetbuysell=BasisExecutionSystem.getBuySell(basisexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultgetbuysell.tolist() == results["getBuySellforBasisExec"]
                resultentercondition=BasisExecutionSystem.enterCondition(basisexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultentercondition.tolist(), results["enterConditionforBasisExec"]
                resultexitcondition=BasisExecutionSystem.exitCondition(basisexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resultexitcondition.tolist() == results["exitConditionforBasisExec"]
                mock_instrument.getCurrentPosition.side_effect=[2,3,0,2,0]
                resulthackcondition=BasisExecutionSystem.hackCondition(basisexecutionsystem,data["prediction"].iloc[-1],mock_instrumentmanager)
                assert resulthackcondition.tolist() == results["hackConditionforBasisExec"]
