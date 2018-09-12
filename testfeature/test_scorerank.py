import os,sys,shutil
sys.path.append(os.path.abspath('..'))
from backtester.features.score_rank_feature import ScoreRankFeature
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

def test_scorerank(mock_instrumentmanager, mock_instrumentlookbackdata):
        initialize = Initialize()
        for i in range(0,5):
                dataSet = initialize.getThirdDataSet(i)
                data=dataSet["data"]
                featureParams=dataSet["featureParams"]
                with pytest.raises(NotImplementedError):
                        ScoreRankFeature.computeForInstrument(i, "", dataSet["featureParams"], "featureKey", mock_instrumentmanager)
                d=OrderedDict()
                d["one"]=mock_instrumentmanager
                d["two"]=mock_instrumentmanager
                d["three"]=mock_instrumentmanager
                if i==0:
                        df1=pd.DataFrame({'featureKey'      :   pd.Series([]),
                                          'predictionKey'   :   pd.Series([]),
                                          'price'           :   pd.Series([]) })
                        df2=pd.DataFrame({'featureKey'      :   pd.Series([]),
                                          'predictionKey'   :   pd.Series([]),
                                          'price'           :   pd.Series([]) })
                        df3=pd.DataFrame({'featureKey'      :   pd.Series([]),
                                          'predictionKey'   :   pd.Series([]),
                                          'price'           :   pd.Series([]) })
                if i==1:
                        df1=pd.DataFrame({'featureKey'      :   pd.Series([1.0]),
                                          'predictionKey'   :   pd.Series([2.0]),
                                          'price'           :   pd.Series([3.0]) })
                        df2=pd.DataFrame({'featureKey'      :   pd.Series([5.02]),
                                          'predictionKey'   :   pd.Series([1.99]),
                                          'price'           :   pd.Series([4.56]) })
                        df3=pd.DataFrame({'featureKey'      :   pd.Series([9.87]),
                                          'predictionKey'   :   pd.Series([6.54]),
                                          'price'           :   pd.Series([1.23]) })
                if i==2:
                        df1=pd.DataFrame({'featureKey'      :   pd.Series([1.23,5.82,6.78,6.37,7.91,1.78]),
                                          'predictionKey'   :   pd.Series([9.25,2.02,3.69,4.12,7.85,4.25]),
                                          'price'           :   pd.Series([7.12,4.15,7.85,9.63,4.56,1.32]) })
                        df2=pd.DataFrame({'featureKey'      :   pd.Series([5.24,8.94,7.16,4.02,0.02,4.63]),
                                          'predictionKey'   :   pd.Series([3.01,1.11,7.89,9.25,4.02,4.16]),
                                          'price'           :   pd.Series([7.19,8.88,4.14,7.99,9.99,1.11]) })
                        df3=pd.DataFrame({'featureKey'      :   pd.Series([2.22,1.11,5.11,6.22,4.88,7.88]),
                                          'predictionKey'   :   pd.Series([0.00,0.02,3.69,4.55,7.34,9.56]),
                                          'price'           :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]) })
                if i==3:
                        df1=pd.DataFrame({'featureKey'      :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'predictionKey'   :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'price'           :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]) })
                        df2=pd.DataFrame({'featureKey'      :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'predictionKey'   :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'price'           :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]) })
                        df3=pd.DataFrame({'featureKey'      :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'predictionKey'   :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]),
                                          'price'           :   pd.Series([4.16,7.89,7.77,7.25,3.33,1.00]) })
                if i==4:
                        df1=pd.DataFrame({'featureKey'      :   pd.Series([np.nan,np.inf,4.44,np.inf]),
                                          'predictionKey'   :   pd.Series([np.inf,0.05,0.00,0.01]),
                                          'price'           :   pd.Series([np.inf,-np.inf,5.12,8.00]) })
                        df2=pd.DataFrame({'featureKey'      :   pd.Series([2.06,np.nan,4.26,0.00]),
                                          'predictionKey'   :   pd.Series([5.26,np.inf,-np.inf,np.inf]),
                                          'price'           :   pd.Series([7.89,7.02,1.36,5.02]) })
                        df3=pd.DataFrame({'featureKey'      :   pd.Series([np.nan,5.02,np.inf,-np.inf]),
                                          'predictionKey'   :   pd.Series([np.nan,0.00,np.inf,-np.inf]),
                                          'price'           :   pd.Series([0.00,0.00,0.00,0.00]) })

                df=pd.DataFrame({'featureKey':data["featureKey"], 'predictionKey': data["predictionKey"], 'price': data["price"]})
                mock_instrumentmanager.getAllInstrumentsByInstrumentId.return_value = d
                mock_instrumentmanager.getDataDf.side_effect=[df,df1,df2,df3,df]
                resultforMarket=ScoreRankFeature.computeForMarket(i, "", dataSet["featureParams"], "featureKey", {}, mock_instrumentmanager)
                #print (resultforMarket)
                assert round(resultforMarket,2) == dataSet["scorer"]
