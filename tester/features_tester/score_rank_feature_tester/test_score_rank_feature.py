import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
from collections import OrderedDict
sys.path.append(os.path.abspath(''))
from backtester.features.score_rank_feature import ScoreRankFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_score_rank_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_score_rank_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,6):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        with pytest.raises(NotImplementedError):
                ScoreRankFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)
        if i!=5:
            dict=OrderedDict()
            dict["one"]=mock_instrumentmanager
            dict["two"]=mock_instrumentmanager
            dict["three"]=mock_instrumentmanager
            mock_instrumentmanager.getDataDf.side_effect=[dataSet["getDataDf"],dataSet["df1"],dataSet["df2"],dataSet["df3"],dataSet["getDataDf"]]
        else:
############ dict is empty, will return 0
            dict={}
            mock_instrumentmanager.getDataDf.side_effect=[dataSet["getDataDf"],dataSet["getDataDf"]]
        mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dict
        assert ScoreRankFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["score_rank_Market"]
