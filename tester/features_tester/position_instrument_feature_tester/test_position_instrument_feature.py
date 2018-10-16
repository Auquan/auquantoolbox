import os,sys,shutil,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.position_instrument_feature import PositionInstrumentFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_position_instrument_feature import *

@pytest.fixture
def mockInstrumentManager():
    return Mock(spec=InstrumentManager)

def test_position_instrument_feature(mockInstrumentManager):
    for i in range (0,2):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        mockInstrumentManager.getAllInstrumentsByInstrumentId.return_value = dataSet["dict"]
        mockInstrumentManager.getInstrument('').getCurrentPosition.side_effect =[10,20]
        result_Instrument=PositionInstrumentFeature.computeForInstrument("", i, parameters, "featureKey", mockInstrumentManager)
######## checking it twice as the return value is not an ordered sequence
        try:
            assert result_Instrument==results["positionInstrument_Instrument1"]
        except:
            assert result_Instrument==results["positionInstrument_Instrument2"]
