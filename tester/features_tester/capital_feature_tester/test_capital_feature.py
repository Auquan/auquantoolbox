import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.capital_feature import CapitalFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_capital_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_capital_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,4):
        data = getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        mock_instrumentmanager.getDataDf.return_value=dataSet["getDataDf"]
######## testing for error causing data
        if i==0 or i==2:
            with pytest.raises(Exception) as e_info:
                CapitalFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)
            # assert CapitalFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)==(results["capital_Instrument"])
######## testing for sample data
        if i==1 or i==3:
            # print(CapitalFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).fillna(0).round(2))
            # print(results["capital_Instrument"])
            assert CapitalFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).fillna(0).round(2).equals(results["capital_Instrument"])
        print(i)
        assert CapitalFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["capital_Market"]
