import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.crossInstrument_correlation_feature import MovingInstrumentCorrelationFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_crossInstrument_correlation_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_crossInstrument_correlation_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,6):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        assert round(MovingInstrumentCorrelationFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager),2)==results["crossInstrument_correlation_Market"]
