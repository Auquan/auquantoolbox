import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.features.portfolio_value_feature import PortfolioValueFeature
from backtester.instruments.instrument import Instrument
from backtester.instruments_manager import *
from unittest.mock import Mock, MagicMock
import math
import pandas as pd
import pytest
from initialize import Initialize
import numpy as np

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)

def test_Portfolio(mock_instrumentmanager):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                resultforMarket=PortfolioValueFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {'pnl':i}, mock_instrumentmanager)
                assert resultforMarket == dataSet["port"]
