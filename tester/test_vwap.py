import numpy as np
import sys
sys.path.append(r'''C:\Users\tejaswini\Desktop\auquantoolbox''')
from backtester.features.vwap_price_feature import VwapPriceInstrumentFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.modelLearningManagers.feature_manager import FeatureManager
from unittest.mock import Mock, MagicMock
from tester.initialize import Initialize
import math
import pandas as pd
import pytest

@pytest.fixture
def mockInstrumentManager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mockFeatureManager():
    return Mock(spec=FeatureManager)
@pytest.fixture
def mockInstrumentLookbackData():
	return Mock(spec=InstrumentsLookbackData)

def test_vwap(mockInstrumentManager, mockFeatureManager, mockInstrumentLookbackData):
    for i in range(1,4):
        dataSet = Initialize.getDataSet(i)
        print(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        resultInstrument = VwapPriceInstrumentFeature.computeForInstrument(i, "", dataSet['featureParams'], 'ma_m', mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet['data']
        with pytest.raises(NotImplementedError):
            VwapPriceInstrumentFeature.computeForMarket(i, "", dataSet['featureParams'], 'ma_m', {}, mockInstrumentManager)
        mockFeatureManager.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        resultInstrumentData = VwapPriceInstrumentFeature.computeForInstrumentData(i, dataSet['featureParams'], 'ma_m', mockFeatureManager )
        assert round(resultInstrument,2) == round(dataSet['vwap'][-1],2)
        assert round(resultInstrumentData.iloc[-1],2) == round(dataSet['vwap'][-1],2)
    for i in range(4,5):
        dataSet = Initialize.getDataSet(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        with pytest.raises(ValueError):
            VwapPriceInstrumentFeature.computeForInstrument(i, "", dataSet['featureParams'], 'ma_m', mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet['data']
        with pytest.raises(NotImplementedError):
            VwapPriceInstrumentFeature.computeForMarket(i, "", dataSet['featureParams'], 'ma_m', {}, mockInstrumentManager)
        mockFeatureManager.getFeatureDf.side_effect = [dataSet['data']['high'], dataSet['data']['high'], dataSet['data']['open'], dataSet['data']['open']]
        with pytest.raises(ValueError):
            VwapPriceInstrumentFeature.computeForInstrumentData(i, dataSet['featureParams'], 'ma_m', mockFeatureManager )
