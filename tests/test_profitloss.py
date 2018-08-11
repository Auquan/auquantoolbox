from backtester.features.profitloss_feature import ProfitLossFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.instruments.instrument import Instrument
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
@pytest.fixture
def mock_instrument():
        return Mock(spec=Instrument)

def test_profitloss(mock_instrumentmanager, mock_instrumentlookbackdata, mock_instrument):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                def sideeffect(value):
                        f=dataSet["featureParams"]
                        if (value=="position"):
                                df=pd.DataFrame(data["position"])
                                df.columns = ['a']
                                return df
                        if (value==f['price']):
                                df=pd.DataFrame(data["price"])
                                df.columns = ['a']
                                return df
                        if (value==f['fees']):
                                df=pd.DataFrame(data["fees"])
                                df.columns = ['a']
                                return df
                        if (value=="featureKey"):
                                df=pd.DataFrame(data["featureKey"])
                                df.columns = ['a']
                                return df
                        if (value=="pnlKey"):
                                df=pd.DataFrame(data["pnlKey"])
                                return df
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                mock_instrumentmanager.getInstrument.return_value=mock_instrument
                mock_instrument.getLastTradePrice.side_effect=[float(i)]
                mock_instrument.getLastTradeLoss.side_effect=[float(5-i)]
                if i==0:
                        with pytest.raises(IndexError):
                                ProfitLossFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                else:
                        resultforInstrument=ProfitLossFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                        assert list(resultforInstrument) == dataSet["pli"]
                mock_instrumentmanager.getDataDf.return_value = pd.DataFrame(data["featureKey"])
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf.return_value= MagicMock(side_effect=sideeffect)
                resultforMarket = ProfitLossFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert resultforMarket == dataSet["plm"]
