import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.features.crossInstrument_correlation_feature import MovingInstrumentCorrelationFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from unittest.mock import Mock, MagicMock
import math
import pandas as pd
import pytest
from initialize import Initialize
import numpy as np

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
        return Mock(spec=InstrumentsLookbackData)

def test_capital(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                def sideeffect(value):
                        if (value=="featureName"):
                                df=pd.DataFrame({'instrumentId1':data["instrumentId1"], 'instrumentId2':data["instrumentId2"]})
                                return df
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultforMarket = MovingInstrumentCorrelationFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert round(resultforMarket,2) == dataSet["ci"]
