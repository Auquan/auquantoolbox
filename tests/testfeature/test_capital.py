import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.features.capital_feature import CapitalFeature
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
        for i in range(1,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                def sideeffect(value):
                        f=dataSet["featureParams"]
                        if (value=="position"):
                                df=data["position"]
                                return df
                        if (value==f['price']):
                                df=data["price"]
                                return df
                        if (value==f['fees']):
                                df=pd.DataFrame(data["fees"])
                                return df
                        if (value=="featureKey"):
                                df=pd.DataFrame(data["featureKey"])
                                return df
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultforInstrument=CapitalFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                mock_instrumentmanager.getDataDf.return_value = data
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultforMarket = CapitalFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert list(resultforInstrument) == [dataSet["cap"]]
                assert resultforMarket == dataSet["capM"]
        for i in range(0,1):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                with pytest.raises(IndexError):
                        CapitalFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                with pytest.raises(IndexError):
                        CapitalFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
