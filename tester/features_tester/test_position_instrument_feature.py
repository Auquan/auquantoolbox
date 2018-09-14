import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
import numpy as np
import sys
from backtester.features.position_instrument_feature import PositionInstrumentFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from unittest.mock import Mock, MagicMock
from collections import OrderedDict
import math
import pytest
import operator
@pytest.fixture
def mockInstrumentManager():
   return Mock(spec=InstrumentManager)

def test_position_instrument_feature(mockInstrumentManager):
   dict = {'a':'okay','b':'notokay'}
   position1 = OrderedDict()
   position1['a'] = 1
   position1['b'] = 2
   position2 = OrderedDict()
   position2['a'] = 2
   position2['b'] = 1

   featureParams  = {'featureName' : 'open'}
   mockInstrumentManager.getAllInstrumentsByInstrumentId.return_value = dict
   mockInstrumentManager.getInstrument('').getCurrentPosition.side_effect = [position1['a'], position1['b']]
   result = PositionInstrumentFeature.computeForInstrument("", "", featureParams, "ma_m", mockInstrumentManager)
   try:
       assert result == position1
   except:
       assert result == position2

   dict = {}
   mockInstrumentManager.getAllInstrumentsByInstrumentId.return_value = dict
   PositionInstrumentFeature.computeForInstrument("", "", featureParams, "ma_m", mockInstrumentManager)
