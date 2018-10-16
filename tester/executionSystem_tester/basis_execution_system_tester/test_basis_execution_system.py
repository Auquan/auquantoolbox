import os,sys,time,pytest, pandas as pd, numpy as np
from datetime import datetime, time, timedelta
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.executionSystem.basis_execution_system import BasisExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import *
from data_basis_execution_system import *

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

def test_basis_execution_system(mock_instrumentmanager, mock_instrumentlookbackdata,mock_instrument):
    for i in range(0,4):
        data = data_basis_execution_system(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        basisexecutionsystem=BasisExecutionSystem(parameters["basisEnter_threshold"],parameters["basisExit_threshold"],
                                                  parameters["basisLongLimit"],parameters["basisShortLimit"],
                                                  parameters["basisCapitalUsageLimit"], parameters["basisLotSize"],
                                                  parameters["basisLimitType"], parameters["basis_thresholdParam"],
                                                  parameters["price"], parameters["feeDict"],parameters["feesRatio"],
                                                  parameters["spreadLimit"],parameters["hackTime"])
######## returning different dataSets
        def sideeffect(value):
            if (value=='close'):
                return dataSet["price"]
            else:
                return dataSet[value]
######## mocking the functions
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dataSet["dict"]
        mock_instrumentmanager.getInstrument.return_value=mock_instrument
######## testing for error producing data
        if i==0 or i==1:
            assert BasisExecutionSystem.getDeviationFromPrediction(basisexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["getDeviationFromPrediction"]
            assert BasisExecutionSystem.getSpread(basisexecutionsystem,mock_instrumentmanager)==results["getSpread"]
            assert BasisExecutionSystem.getFees(basisexecutionsystem,mock_instrumentmanager)==results["getFees"]
            assert BasisExecutionSystem.getBuySell(basisexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["getBuySell"]
            assert BasisExecutionSystem.enterCondition(basisexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["enterCondition"]
            assert BasisExecutionSystem.exitCondition(basisexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["exitCondition"]
            assert BasisExecutionSystem.hackCondition(basisexecutionsystem,pd.DataFrame(),mock_instrumentmanager)==results["hackCondition"]
######## testing for sample data
        else:
            assert BasisExecutionSystem.getDeviationFromPrediction(basisexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).round(2).equals(results["getDeviationFromPrediction"])
            assert BasisExecutionSystem.getSpread(basisexecutionsystem,mock_instrumentmanager).round(2).equals(results["getSpread"])
            assert BasisExecutionSystem.getFees(basisexecutionsystem,mock_instrumentmanager).round(6).equals(results["getFees"])
            assert BasisExecutionSystem.getBuySell(basisexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["getBuySell"])
            assert BasisExecutionSystem.enterCondition(basisexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["enterCondition"])
            mock_instrument.getCurrentPosition.side_effect=parameters["getCurrentPosition"]
            assert BasisExecutionSystem.exitCondition(basisexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["exitCondition"])
            mock_instrument.getCurrentPosition.side_effect=parameters["getCurrentPosition"]
            assert BasisExecutionSystem.hackCondition(basisexecutionsystem,dataSet["prediction"].iloc[-1],mock_instrumentmanager).equals(results["hackCondition"])
