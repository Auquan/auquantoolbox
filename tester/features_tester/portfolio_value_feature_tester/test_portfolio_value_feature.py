import os,sys,shutil,pandas as pd,pytest,numpy as np
from unittest.mock import Mock, MagicMock
sys.path.append(os.path.abspath('../../..'))
from backtester.features.portfolio_value_feature import PortfolioValueFeature
from backtester.instruments.instrument import Instrument
from backtester.instruments_manager import *
from data_portfolio_value_feature import *

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)

def test_portfolio_value_feature(mock_instrumentmanager):
    for i in range(0,4):
        data=getDataSet(i)
        dataSet=data["dataSet"]
        parameters=data["parameters"]
        results=data["results"]
        assert PortfolioValueFeature.computeForMarket(i, "", parameters, "featureKey", dataSet["currentMarketFeatures"], mock_instrumentmanager)==results["portfoliovalue_Market"]
