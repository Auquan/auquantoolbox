import os,sys,shutil,pandas as pd,pytest,numpy as np
from collections import OrderedDict
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.features.crossSectionMomentum_feature import CrossSectionMomentumFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_crossSectionMomentum_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_crossSectionMomentum_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,6):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        d=OrderedDict()
        d["one"]=mock_instrumentmanager
        d["two"]=mock_instrumentmanager
        d["three"]=mock_instrumentmanager
        d["four"]=mock_instrumentmanager
        d["five"]=mock_instrumentmanager
        d["six"]=mock_instrumentmanager
        mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value = d
        mock_instrumentmanager.getDataDf.side_effect=[dataSet["df1"],dataSet["df2"],dataSet["df3"],dataSet["df4"],dataSet["df5"],dataSet["df6"]]
        assert CrossSectionMomentumFeature.computeForMarket(i,"",parameters,"featureKey",{}, mock_instrumentmanager).round(3).equals(results["crossSectionMomentum"])
