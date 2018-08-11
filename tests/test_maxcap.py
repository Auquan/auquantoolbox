from backtester.features.maxcapitalusage_feature import MaxCapitalUsageFeature
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
                with pytest.raises(NotImplementedError):
                    MaxCapitalUsageFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                mock_instrumentmanager.getDataDf.return_value = pd.DataFrame({'capital': data["capital"], 'featureKey' : data["featureKey"]})
                resultforMarket = MaxCapitalUsageFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert resultforMarket == dataSet["maxc"]
