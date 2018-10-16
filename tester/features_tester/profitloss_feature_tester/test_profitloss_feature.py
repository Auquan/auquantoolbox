import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.profitloss_feature import ProfitLossFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import Instrument
from data_profitloss_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)
@pytest.fixture
def mock_instrument():
    return Mock(spec=Instrument)

def test_profitloss_feature(mock_instrumentmanager, mock_instrumentlookbackdata, mock_instrument):
    for i in range(0,4):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        mock_instrumentmanager.getInstrument.return_value=mock_instrument
        mock_instrument.getLastTradePrice.side_effect=[1,2,3,4,5,6,7,8,9]
        mock_instrument.getLastTradeLoss.side_effect=[9,8,7,6,5,4,3,2,1]
        mock_instrumentmanager.getDataDf.return_value=dataSet["getDataDf"]
######## testing for error causing data
        if i==0:
            assert ProfitLossFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)==results["profitloss_Instrument"]
######## sample data
        else:
            assert ProfitLossFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).round(2).equals(results["profitloss_Instrument"])
        assert ProfitLossFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["profitloss_Market"]
