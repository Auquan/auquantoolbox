import os,sys,shutil,pandas as pd,pytest,numpy as np
from unittest.mock import Mock, MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.features.fees_feature import FeesFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_fees_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_fees_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,5):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
######## testing for error causing data
        if i==0 or i==4:
            assert FeesFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)==results["fees_Instrument"]
######## testing for sample data
        if  i in range (1,4):
            assert FeesFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).round(2).equals(results["fees_Instrument"])
        with pytest.raises(NotImplementedError):
            FeesFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)
