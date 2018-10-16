import os,sys,shutil,pandas as pd,pytest,numpy as np
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
sys.path.append(os.path.abspath(''))
from backtester.features.score_fairvalue_feature import ScoreFairValueFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from data_score_fairvalue_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
    return Mock(spec=InstrumentsLookbackData)

def test_score_fairvalue_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
    for i in range(0,5):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        def sideeffect(value):
            return dataSet[value]
        mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
        mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dataSet["dict"]
        mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
        mock_instrumentmanager.getDataDf.return_value = dataSet["getDataDf"]
######## error causing dataSet
        if i==0:
            assert ScoreFairValueFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager)==results["score_fairvalue_Instrument"]
######## updateNum is 0
        elif i==4:
            #testing the series row by row as the rows are not in ordered sequence
            assert ScoreFairValueFeature.computeForInstrument(0, "", parameters, "featureKey", mock_instrumentmanager)['a']==results["score_fairvalue_Instrument"]['a']
            assert ScoreFairValueFeature.computeForInstrument(0, "", parameters, "featureKey", mock_instrumentmanager)['b']==results["score_fairvalue_Instrument"]['b']
######### sample data
        else:
            assert ScoreFairValueFeature.computeForInstrument(i, "", parameters, "featureKey", mock_instrumentmanager).round(3).equals(results["score_fairvalue_Instrument"])
        assert ScoreFairValueFeature.computeForMarket(i, "", parameters, "featureKey", {}, mock_instrumentmanager)==results["score_fairvalue_Market"]
