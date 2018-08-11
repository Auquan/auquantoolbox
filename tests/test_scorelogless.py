from backtester.features.score_logloss_feature import ScoreLogLossFeature
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

def test_scorelogless(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                def sideeffect(value):
                        data=dataSet["data"]
                        if (value=='predictionKey'):
                                df=pd.DataFrame(data["predictionKey"])
                                df.columns = ['a']
                                return df
                        if (value=='featureKey'):
                                df=pd.DataFrame(data["featureKey"])
                                df.columns = ['a']
                                return df
                        if (value=='target'):
                                df=pd.DataFrame(data["target"])
                                df.columns = ['a']
                                return df
                        if (value=='score'):
                                df=pd.DataFrame(data["score"])
                                df.columns = ['a']
                                return df
                dict={'a':1}
                mock_instrumentmanager.getLookbackInstrumentFeatures.return_value = mock_instrumentlookbackdata
                mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value=dict
                mock_instrumentlookbackdata.getFeatureDf=MagicMock(side_effect=sideeffect)
                if i==0:
                        with pytest.raises(IndexError):
                                ScoreLogLossFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                else:
                        resultforInstrument=ScoreLogLossFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                        assert list(np.around(np.array(list(resultforInstrument)),2)) == dataSet["scrli"]
                mock_instrumentmanager.getDataDf.return_value = dataSet["data"]
                resultforMarket = ScoreLogLossFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert [round(resultforMarket,2)] == dataSet["scrlm"]
