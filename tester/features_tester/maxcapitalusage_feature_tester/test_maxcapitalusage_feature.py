import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.maxcapitalusage_feature import MaxCapitalUsageFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_maxcapitalusage_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_maxcapitalusage_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,5):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        mock_instrumentmanager.getDataDf.return_value=dataSet["getDataDf"]
        with pytest.raises(NotImplementedError):
            MaxCapitalUsageFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)
        assert MaxCapitalUsageFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["maxcapitalusage_Market"]
