import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.executionSystem.base_execution_system import InstrumentExection, BaseExecutionSystem
from backtester.instruments_manager import *
from unittest.mock import Mock
import pytest

#mocking InstrumentManager
@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)

def test_base_execution_system(mock_instrumentmanager):
        dict={'1':1,'2':2}
        # InstrumentExection testing
        instrumentexection=InstrumentExection("01/01/2010",dict,10,"abc")
        assert InstrumentExection.getTimeOfExecution(instrumentexection) == "01/01/2010"
        assert InstrumentExection.getInstrumentId(instrumentexection) == dict
        assert InstrumentExection.getVolume(instrumentexection) == 10
        assert InstrumentExection.getExecutionType(instrumentexection) == "abc"
        #BaseExecutionSystem testing
        baseexecutionsystem=BaseExecutionSystem()
        assert BaseExecutionSystem.getExecutions(baseexecutionsystem,"01/01/2010",mock_instrumentmanager,10) == []
        assert BaseExecutionSystem.getExecutionsAtClose(baseexecutionsystem,"01/01/2010", mock_instrumentmanager) == []
