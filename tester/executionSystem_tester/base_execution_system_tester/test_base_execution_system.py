import os,sys,pytest
from unittest.mock import Mock
sys.path.append(os.path.abspath('../../..'))
from backtester.executionSystem.base_execution_system import *
from backtester.instruments_manager import *
from data_base_execution_system import *

#mocking InstrumentManager
@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)

def test_base_execution_system(mock_instrumentmanager):
    data=data_base_execution_system()
    parameters=data["parameters"]
    results=data["results"]
#### InstrumentExection testing
    instrumentexection=InstrumentExection(parameters["time"],parameters["instrumentId"],
                                          parameters["volume"],parameters["executionType"])
    assert InstrumentExection.getTimeOfExecution(instrumentexection) == parameters["time"]
    assert InstrumentExection.getInstrumentId(instrumentexection) == parameters["instrumentId"]
    assert InstrumentExection.getVolume(instrumentexection) == parameters["volume"]
    assert InstrumentExection.getExecutionType(instrumentexection) == parameters["executionType"]
#### BaseExecutionSystem testing
    baseexecutionsystem=BaseExecutionSystem()
    assert BaseExecutionSystem.getExecutions(baseexecutionsystem,parameters["time"],mock_instrumentmanager,parameters["capital"]) == results["getExecutions"]
    assert BaseExecutionSystem.getExecutionsAtClose(baseexecutionsystem,parameters["time"], mock_instrumentmanager) == results["getExecutionsAtClose"]
