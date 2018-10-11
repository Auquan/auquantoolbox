import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.features.maxDrawdown_feature import MaxDrawdownFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_maxDrawdown_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_maxDrawdown_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,8):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        with pytest.raises(NotImplementedError):
            MaxDrawdownFeature.computeForInstrument(i, "",parameters, "featureKey", mock_instrumentmanager)
        mock_instrumentmanager.getDataDf.return_value=dataSet
        assert MaxDrawdownFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["maxDrawdown_Market"]
