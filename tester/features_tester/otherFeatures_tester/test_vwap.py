import numpy as np
import sys, os
sys.path.append(os.path.abspath(''))
from backtester.features.vwap_price_feature import VwapPriceInstrumentFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock,MagicMock
from initialize import Initialize
import math
import pandas as pd
import pytest

@pytest.fixture
def mockInstrumentManager():
    return Mock(spec=InstrumentManager)

@pytest.fixture
def mockInstrumentLookbackData():
	return Mock(spec=InstrumentsLookbackData)

def test_vwap(mockInstrumentManager, mockInstrumentLookbackData):
    for i in range(1,4):
        k = Initialize()
        dataSet = k.getDataSet(i)
        print(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        resultInstrument = VwapPriceInstrumentFeature.computeForInstrument(i, "", dataSet['featureParams'], 'ma_m', mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet['data']
        with pytest.raises(NotImplementedError):
            VwapPriceInstrumentFeature.computeForMarket(i, "", dataSet['featureParams'], 'ma_m', {}, mockInstrumentManager)
        assert round(resultInstrument,2) == round(dataSet['vwap'][-1],2)
    for i in range(4,5):
        k = Initialize()
        dataSet = k.getDataSet(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        with pytest.raises(ValueError):
            VwapPriceInstrumentFeature.computeForInstrument(i, "", dataSet['featureParams'], 'ma_m', mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet['data']
        with pytest.raises(NotImplementedError):
            VwapPriceInstrumentFeature.computeForMarket(i, "", dataSet['featureParams'], 'ma_m', {}, mockInstrumentManager)
