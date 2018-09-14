import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.features.count_loss_feature import CountLossFeature
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

def test_count_loss_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                def sideeffect(value):
                        data=dataSet["data"]
                        if (value=='pnlKey'):
                                df=pd.DataFrame(data["pnlKey"])
                                df.columns = ['a']
                                return df
                        if (value=='featureKey'):
                                df=pd.DataFrame(data["featureKey"])
                                df.columns = ['a']
                                return df
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                resultforInstrument=CountLossFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                mock_instrumentmanager.getDataDf.return_value = dataSet["data"]
                resultforMarket = CountLossFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert (resultforInstrument.tolist()) == dataSet["cntli"]
                assert [float(resultforMarket)] == dataSet["cntlm"]
