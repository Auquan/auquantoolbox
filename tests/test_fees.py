from backtester.features.fees_feature import FeesFeature
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

def test_Fees(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(1,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                def sideeffect(value):
                        f=dataSet["featureParams"]
                        if (value=="position"):
                                df=pd.DataFrame(data["positionFees"])
                                return df
                        if (value==f['price']):
                                df=data["price"]
                                return df
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultforInstrument=FeesFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                with pytest.raises(NotImplementedError):
                        FeesFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert list(resultforInstrument) == list(dataSet["fees"])
        for i in range(0,1):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                with pytest.raises(IndexError):
                        resultforInstrument=FeesFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                with pytest.raises(NotImplementedError):
                        FeesFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
