import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.executionSystem.base_execution_system import *
from backtester.executionSystem.pair_execution_system import PairExecutionSystem
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.lookback_data import LookbackData
from datetime import datetime
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import math
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
@pytest.fixture
def mock_lookbackdata():
    return Mock(spec=LookbackData)

def test_pairexec(mock_instrumentmanager, mock_instrumentlookbackdata,mock_lookbackdata):
        initialize = Initialize()
        for i in range(1,6):
                if i==3:
                        continue
                dataSet = initialize.getDataSet(i)
                data=dataSet["dataSet"]
                parameters=dataSet["parameters"]
                def sideeffect(value):
                        if (value=='close'):
                                return data["price"].iloc[:,[0,1]]
                        if (value=='position'):
                                return data["position"].iloc[:,[0,1]]
                        if (value=='prediction'):
                                return data["prediction"].iloc[:,[0,1]]
                pairexecutionsystem=PairExecutionSystem(parameters["pair"],parameters["pairRatio"],parameters["pairEnter_threshold"],
                                                        parameters["pairExit_threshold"],parameters["pairLongLimit"],
                                                        parameters["pairShortLimit"],parameters["pairCapitalUsageLimit"],
                                                        parameters["pairLotSize"],parameters["priceforSimpleExec"])
                dict={'prediction':data["prediction"]}
                time = datetime(2018, 6, 1)
                mock_instrumentmanager.getLookbackMarketFeatures.return_value = mock_lookbackdata
                mock_lookbackdata.getData.return_value=dict
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultgetexecutions=PairExecutionSystem.getExecutions(pairexecutionsystem,time,mock_instrumentmanager,parameters["capital"])
                count = 0
                for x in resultgetexecutions:
                        assert isinstance(x,InstrumentExection)
                        count +=1
                assert count == parameters["countforpairvalue"]
