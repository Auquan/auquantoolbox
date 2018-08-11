from backtester.features.maxDrawdown_feature import MaxDrawdownFeature
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

def test_maxcapital(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                featureParams=dataSet["featureParams"]
                with pytest.raises(NotImplementedError):
                        MaxDrawdownFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                series1=pd.Series({0:featureParams["dict1"], 1: featureParams["dict2"]})
                df={'featureKey': series1, 'portfolio_value': data["maxdraw"]}
                mock_instrumentmanager.getDataDf.return_value = df
                if i==3:
                        with pytest.raises(KeyError):
                                MaxDrawdownFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                elif i==4:
                        with pytest.raises(TypeError):
                                MaxDrawdownFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                else:
                        resultforMarket = MaxDrawdownFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                        assert resultforMarket == dataSet["maxd"]
