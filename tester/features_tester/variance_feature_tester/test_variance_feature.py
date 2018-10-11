import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.features.variance_feature import VarianceFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_variance_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_variance_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,5):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def side_effect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value = dataSet["dict"]
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=side_effect)
        mock_instrumentmanager.getDataDf.return_value = dataSet["getDataDf"]
        assert VarianceFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).round(3).equals(results["variance_Instrument"])
        assert round(VarianceFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager),3)==results["variance_Market"]
