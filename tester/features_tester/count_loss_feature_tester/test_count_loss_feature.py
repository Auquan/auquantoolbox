import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.count_loss_feature import CountLossFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_count_loss_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_count_loss_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range (0,4):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        mock_instrumentmanager.getDataDf.return_value = dataSet["getDataDf"]
######## testing for error causing data
        if i==0:
            assert CountLossFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)==results["count_loss_Instrument"]
######## testing for sample data
        if i in range (1,4):
            assert CountLossFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).equals(results["count_loss_Instrument"])
        assert CountLossFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["count_loss_Market"]
