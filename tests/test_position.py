import numpy as np
import sys
from backtester.features.position_instrument_feature import PositionInstrumentFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.modelLearningManagers.feature_manager import FeatureManager
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import math
import pytest
import operator
@pytest.fixture
def mockInstrumentManager():
   return Mock(spec=InstrumentManager)

def test_positionInstrument(mockInstrumentManager):
   dict = {'a':'okay','b':'notokay'}
   position = OrderedDict()
   position['a'] = 1
   position['b'] = 2

   featureParams  = {'featureName' : 'open'}
   mockInstrumentManager.getAllInstrumentsByInstrumentId.return_value = dict
   mockInstrumentManager.getInstrument('').getCurrentPosition.side_effect = [position['a'], position['b']]
   result = PositionInstrumentFeature.computeForInstrument("", "", featureParams, "ma_m", mockInstrumentManager)
   assert result == position

   dict = {}
   mockInstrumentManager.getAllInstrumentsByInstrumentId.return_value = dict
   with pytest.raises(ValueError):
       PositionInstrumentFeature.computeForInstrument("", "", featureParams, "ma_m", mockInstrumentManager)
