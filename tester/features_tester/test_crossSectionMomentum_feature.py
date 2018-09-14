import os,sys,shutil
sys.path.append(os.path.abspath('../..'))
from backtester.features.crossSectionMomentum_feature import CrossSectionMomentumFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from unittest.mock import Mock, MagicMock
import math
import pandas as pd
import pytest
from initialize import Initialize
import numpy as np
from collections import OrderedDict

@pytest.fixture
def mock_instrumentmanager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mock_instrumentlookbackdata():
        return Mock(spec=InstrumentsLookbackData)

def test_crossSectionMomentum_feature(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                d=OrderedDict()
                d["one"]=mock_instrumentmanager
                d["two"]=mock_instrumentmanager
                d["three"]=mock_instrumentmanager
                d["four"]=mock_instrumentmanager
                d["five"]=mock_instrumentmanager
                d["six"]=mock_instrumentmanager
                if i==0:
                        df1=pd.Series({'featureName':[]})
                        df2=pd.Series({'featureName':[]})
                        df3=pd.Series({'featureName':[]})
                        df4=pd.Series({'featureName':[]})
                        df5=pd.Series({'featureName':[]})
                        df6=pd.Series({'featureName':[]})
                        result= pd.Series({'one' : 0.0, 'two' : 0.0, 'three' : 0.0, 'four': 0.0, 'five': 0.0, 'six': 0.0})
                if i==1:
                        df1=pd.Series({'featureName':[1.0]})
                        df2=pd.Series({'featureName':[1.0]})
                        df3=pd.Series({'featureName':[8.0]})
                        df4=pd.Series({'featureName':[9.0]})
                        df5=pd.Series({'featureName':[18.0]})
                        df6=pd.Series({'featureName':[11.0]})
                        result= pd.Series({'one' : 0.0, 'two' : 0.0, 'three' : 0.0, 'four': 0.0, 'five': 0.0, 'six': 0.0})

                if i==2:
                        df1=pd.Series({'featureName':[1,2,3,4,5,6,7,8,9]})
                        df2=pd.Series({'featureName':[1,3,5,7,9,11,13,15,17]})
                        df3=pd.Series({'featureName':[8,5,2,6,5,4,7,9,0]})
                        df4=pd.Series({'featureName':[9,5,1,7,5,3,8,4,2]})
                        df5=pd.Series({'featureName':[18,16,14,12,10,8,6,4,2]})
                        df6=pd.Series({'featureName':[11,14,17,3,6,9,2,5,8]})
                        result= pd.Series({'one' : 0.62, 'two' : 1.33, 'three' : -0.27, 'four': -0.29, 'five': -0.84, 'six': -0.55})
                if i==3:
                        df1=pd.Series({'featureName':[1,2,3,4,5,6,7,8,9]})
                        df2=pd.Series({'featureName':[1,3,5,7,9,11,13,15,17]})
                        df3=pd.Series({'featureName':[8,5,2,6,5,4,7,9,0]})
                        df4=pd.Series({'featureName':[9,5,1,7,5,3,8,4,2]})
                        df5=pd.Series({'featureName':[18,16,14,12,10,8,6,4,2]})
                        df6=pd.Series({'featureName':[11,14,17,3,6,9,2,5,8]})
                        result= pd.Series({'one' : 0.0, 'two' : 0.0, 'three' : 0.0, 'four': 0.0, 'five': 0.0, 'six': 0.0})
                if i==4:
                        df1=pd.Series({'featureName':[1.0,np.nan,np.inf,-np.inf]})
                        df2=pd.Series({'featureName':[1.0,3.0,np.inf,7.0]})
                        df3=pd.Series({'featureName':[-np.inf,5.0,np.nan,6.0]})
                        df4=pd.Series({'featureName':[np.nan,np.inf,1.0,-np.inf]})
                        df5=pd.Series({'featureName':[18.0,16.0,14.0,12.0]})
                        df6=pd.Series({'featureName':[11.0,14.0,np.inf,3.0]})
                        result= pd.Series({'one' : -0.33, 'two' : 1.42, 'three' : -0.33, 'four': -0.33, 'five': -0.16, 'six': -0.26})

                mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value = d
                mock_instrumentmanager.getDataDf=Mock()
                mock_instrumentmanager.getDataDf.side_effect=[df1,df2,df3,df4,df5,df6]
                resultforMarket = CrossSectionMomentumFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                assert resultforMarket['one'].round(2) == result["one"]
                assert resultforMarket['two'].round(2) == result["two"]
                assert resultforMarket['three'].round(2) == result["three"]
                assert resultforMarket['four'].round(2) == result["four"]
                assert resultforMarket['five'].round(2) == result["five"]
                assert resultforMarket['six'].round(2) == result["six"]
