import pandas as pd
import numpy as np
class Initialize(object):

########################################################################################################################################################################################################################
########################################################################################################################################################################################################################
########################################################################################################################################################################################################################

    def getThirdDataSet(self,c):
        data = pd.DataFrame()
        if(c==0):
            data["position"] = []
            data["price"] = []
            data["fees"] = []
            data["featureKey"] = []
            data["capital"] = []
            data["positionFees"] = []
            data["instrumentId1"] = []
            data["instrumentId2"] = []
            data["maxdraw"] = []
            data["pnlKey"] =[]
            data["score"] =[]
            data["target"] =[]
            data["predictionKey"] =[]
            featureParams  = {"position" : "position", "price" : "price", "fees": "fees", "featureKey" : "featureKey", "initial_capital" : 5.0, "period" : 1, "capitalKey" : "capital", "portfolioValueKey" : "portfolio_value","target":"target",
                              "feesDict" : {0:0, -1:-1, 1:1}, "positionFees" : "positionFees",'pnl': 'pnl', 'instrumentId1':'instrumentId1', 'instrumentId2':'instrumentId2', 'featureName': 'featureName', "predictionKey": "predictionKey",
                              "dict1":{'maxPortfolioValue': 5.85 , 'maxDrawdown': 10.01},"dict2":{'maxPortfolioValue': 0.95 , 'maxDrawdown': 1.56}, "instrument_pnl_feature" : 'pnlKey',"pnlKey" : "pnlKey","instrument_score_feature": "score"}
            return {"data" : data, "featureParams" : featureParams, 'cap'   :   14.0,
                                                                    'capM'  :   5.0,
                                                                    'fees'  :   [3.0],
                                                                    'pos'   :   {},
                                                                    'port'  :   5.0,
                                                                    'ci'    :   0,
                                                                    'maxc'  :   0,
                                                                    'scorer':   0.0,
                                                                    'pli'   :   [0.0],
                                                                    'plm'   :   0.0,
                                                                    'vari'  :   0.0,
                                                                    'varm'  :   [0.0],
                                                                    'totpi' :   [0.0],
                                                                    'totpm' :   [0.0],
                                                                    'totli' :   [0.0],
                                                                    'totlm' :   [0.0],
                                                                    'cntpi' :   [0.0],
                                                                    'cntpm' :   [0.0],
                                                                    'cntli' :   [0.0],
                                                                    'cntlm' :   [0.0],
                                                                    'scrfi' :   [0.0],
                                                                    'scrfm' :   [0.0],
                                                                    'scrli' :   [0.0],
                                                                    'scrlm' :   [0.0],
                                                                    'maxd'  :   {'maxDrawdown': 0.0, 'maxPortfolioValue': 0.0}}
        if(c==1):
            data["position"] = [1.0]
            data["price"] = [9.0]
            data["fees"] = [5.0]
            data["featureKey"] = [3.0]
            data["capital"] = [2.0]
            data["positionFees"] = [0]
            data["instrumentId1"] = [2.58]
            data["instrumentId2"] = [3.14]
            data["maxdraw"] = [5.14]
            data["pnlKey"] =[3.14]
            data["score"] =[3.14]
            data["target"] =[3.14]
            data["predictionKey"] =[0.5]
            featureParams  = {"position" : "position", "price" : "price", "fees": "fees", "featureKey" : "featureKey", "initial_capital" : 5.0, "period" : 1, "capitalKey" : "capital", "portfolioValueKey" : "portfolio_value","target":"target",
                              "feesDict" : {0:0, -1:-1, 1:1}, "positionFees" : "positionFees",'pnl': 'pnl', 'instrumentId1':'instrumentId1', 'instrumentId2':'instrumentId2', 'featureName': 'featureName',"predictionKey": "predictionKey",
                              "dict1":{'maxPortfolioValue': 5.85 , 'maxDrawdown': 10.01},"dict2":{'maxPortfolioValue': 0.95 , 'maxDrawdown': 1.56}, "instrument_pnl_feature" : 'pnlKey',"pnlKey" : "pnlKey","instrument_score_feature": "score"}
            return {"data" : data, "featureParams" : featureParams, 'cap'   :   14.0,
                                                                    'capM'  :   5.0,
                                                                    'fees'  :   [0.0],
                                                                    'pos'   :   {1.0: 1},
                                                                    'port'  :   6.0,
                                                                    'ci'    :   0,
                                                                    'maxc'  :   0,
                                                                    'scorer':   0.0,
                                                                    'plm'   :   3.14,
                                                                    'pli'   :   [2.0],
                                                                    'vari'  :   [0.0],
                                                                    'varm'  :   [0.0],
                                                                    'totpi' :   [3.14],
                                                                    'totpm' :   [3.14],
                                                                    'totli' :   [0.0],
                                                                    'totlm' :   [0.0],
                                                                    'cntpi' :   [1.0],
                                                                    'cntpm' :   [1.0],
                                                                    'cntli' :   [0.0],
                                                                    'cntlm' :   [0.0],
                                                                    'scrfi' :   [8.5],
                                                                    'scrfm' :   [0.00],
                                                                    'scrli' :   [0.69],
                                                                    'scrlm' :   [3.14],
                                                                    'maxd'  :   {'maxDrawdown': 0.0, 'maxPortfolioValue': 0.0} }

        if(c==2):
            data["position"] = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]
            data["price"] = [9.0,8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0]
            data["fees"] = [9.0,8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0]
            data["featureKey"] = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]
            data["capital"] = [1.0,-5.0,2.0,-9.0,7.0,0.0,-8.0,-5.0,8.0]
            data["positionFees"] = [1, -8, 0, -4, 0, -5, -8, 2, 3]
            data["instrumentId1"] = [1.20,2.64,3.89,0.48,9.06,-6.52,2.46,3.76,7.80]
            data["instrumentId2"] = [3.14,2.82,-1.98,5.67,4.65,7.89,4.98,9.02,-2.87]
            data["maxdraw"] = [1.04,2.78,3.87,4.45,5.96,6.78,3.89,0.48,9.06]
            data["pnlKey"] =[1.04,2.78,3.87,4.45,5.96,6.78,3.89,0.48,9.06]
            data["score"] =[3.14,2.82,-1.98,1.04,2.78,3.87,9.06,-6.52,2.46]
            data["target"] =[3.14,2.82,-1.98,1.04,2.78,3.87,9.06,-6.52,2.46]
            data["predictionKey"] =[1.04,2.78,3.87,4.45,5.96,6.78,3.89,0.48,0.06]
            featureParams  = {"position" : "position", "price" : "price", "fees": "fees", "featureKey" : "featureKey", "initial_capital" : 5.0, "period": 5, "capitalKey" : "capital", "portfolioValueKey" : "portfolio_value","target":"target",
                              "feesDict" : {0:0, -1:-1, 1:1}, "positionFees" : "positionFees",'pnl': 'pnl', 'instrumentId1':'instrumentId1', 'instrumentId2':'instrumentId2', 'featureName': 'featureName', "predictionKey": "predictionKey",
                              "dict1":{'maxPortfolioValue': 5.85 , 'maxDrawdown': 10.01},"dict2":{'maxPortfolioValue': 0.95 , 'maxDrawdown': 1.56}, "instrument_pnl_feature" : 'pnlKey',"pnlKey" : "pnlKey","instrument_score_feature": "score"}
            return {"data" : data, "featureParams" : featureParams, 'cap'   :   -5.0,
                                                                    'capM'  :   -1.0,
                                                                    'fees'  :   [1.0],
                                                                    'pos'   :   {0.0: 2, 1.0: 2, 2.0: 2, 3.0: 2, 4.0: 2, 5.0: 2, 6.0: 2, 7.0: 2, 8.0: 2},
                                                                    'port'  :   7.0,
                                                                    'ci'    :   -0.56,
                                                                    'maxc'  :   10.0 ,
                                                                    'scorer':   3.88,
                                                                    'plm'   :   9.06,
                                                                    'pli'   :   [-4.0],
                                                                    'vari'  :   [79.79],
                                                                    'varm'  :   [79.29],
                                                                    'totpi' :   [16.58],
                                                                    'totpm' :   [15.58],
                                                                    'totli' :   [8.0],
                                                                    'totlm' :   [7.0],
                                                                    'cntpi' :   [9.0],
                                                                    'cntpm' :   [8.0],
                                                                    'cntli' :   [8.0],
                                                                    'cntlm' :   [7.0],
                                                                    'scrfi' :   [5.7],
                                                                    'scrfm' :   [2.46],
                                                                    'scrli' :   [7.42],
                                                                    'scrlm' :   [2.46],
                                                                    'maxd'  :   {'maxDrawdown': 10.01, 'maxPortfolioValue': 9.06}}
        if(c==3):
            data["position"] = [2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
            data["price"] = [9.0,8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0,]
            data["fees"] = [10.0,9.0,8.0,7.0,6.0,5.0,4.0,3.0,2.0]
            data["featureKey"] = [9.0,8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0]
            data["capital"] = [1.0,-5.0,2.0,-9.0,7.0,0.0,-8.0,-3.0,4.0]
            data["positionFees"] = [1, -8, 0, -5, 3, -4, -6, 0, 2]
            data["instrumentId1"] = [1.20,2.64,3.89,0.48,9.06,-6.52,2.46,3.76,7.80]
            data["instrumentId2"] = [3.14,2.82,-1.98,5.67,4.65,7.89,4.98,9.02,-2.87]
            data["maxdraw"] = [1.20,2.64,3.89,4.45,5.96,6.78,3.14,2.82,-1.98]
            data["pnlKey"] =[1.20,2.64,3.89,4.45,5.96,6.78,3.14,2.82,-1.98]
            data["score"] =[1.20,2.64,3.89,6.78,3.14,2.82,4.45,5.96,6.78]
            data["target"] =[1.20,2.64,3.89,6.78,3.14,2.82,4.45,5.96,6.78]
            data["predictionKey"] =[1.04,2.78,3.87,4.45,5.96,6.78,3.89,0.48,0.24]
            featureParams  = {"position" : "position", "price" : "price", "fees": "fees", "featureKey" : "featureKey", "initial_capital" : 5.0, "period" : 11, "capitalKey" : "capital", "portfolioValueKey" : "portfolio_value",
                              "feesDict" : {0:0, -1:-1, 1:1}, "positionFees" : "positionFees",'pnl': 'pnl', 'instrumentId1':'instrumentId1', 'instrumentId2':'instrumentId2', 'featureName': 'featureName', "predictionKey": "predictionKey",
                              "dict1":{},"dict2":{}, "instrument_pnl_feature" : 'pnlKey',"pnlKey" : "pnlKey","instrument_score_feature": "score","target":"target"}
            return {"data" : data, "featureParams" : featureParams, 'cap'   :   -6.0,
                                                                    'capM'  :   1.0,
                                                                    'fees'  :   [2.0],
                                                                    'pos'   :   {2.0: 3, 3.0: 3, 4.0: 3, 5.0: 3, 6.0: 3, 7.0: 3, 8.0: 3, 9.0: 3, 10.0: 3},
                                                                    'port'  :   8.0,
                                                                    'ci'    :   0,
                                                                    'maxc'  :   8.0 ,
                                                                    'scorer':   0.0,
                                                                    'plm'   :   -1.98,
                                                                    'pli'   :   [-14.0],
                                                                    'vari'  :   [11.64],
                                                                    'varm'  :   [12.31],
                                                                    'totpi' :   [1.0],
                                                                    'totpm' :   [2.0],
                                                                    'totli' :   [5.8],
                                                                    'totlm' :   [6.8],
                                                                    'cntpi' :   [1.0],
                                                                    'cntpm' :   [2.0],
                                                                    'cntli' :   [2.0],
                                                                    'cntlm' :   [3.0],
                                                                    'scrfi' :   [0.93],
                                                                    'scrfm' :   [6.78],
                                                                    'scrli' :   [3.36],
                                                                    'scrlm' :   [6.78],
                                                                    'maxd'  :   {'maxDrawdown': 10.01, 'maxPortfolioValue': 5.85}}
        if(c==4):
            data["position"] = [np.nan,2.0, np.inf,2.0]
            data["price"] = [np.inf,-np.inf,np.nan,3.0]
            data["fees"] = [0.0,-np.inf,np.inf,-np.inf]
            data["featureKey"] = [np.inf,-np.inf,np.nan,3.0]
            data["capital"] = [-np.inf,1.0,-3.0,4.0]
            data["positionFees"] = [np.inf, -3, np.nan, 1]
            data["instrumentId1"] = [np.inf,np.nan,-np.inf,2.35]
            data["instrumentId2"] = [0.96,np.nan,np.nan,np.nan]
            data["maxdraw"] = [np.inf,-np.inf,np.inf,np.nan]
            data["pnlKey"] =[np.inf,-np.inf,np.inf,1.25]
            data["score"] =[2.00,np.nan,-np.inf,5.42]
            data["target"] =[2.00,np.nan,-np.inf,5.42]
            data["predictionKey"] =[np.inf,-np.inf,np.inf,0.42]
            featureParams  = {"position" : "position", "price" : "price", "fees": "fees", "featureKey" : "featureKey", "initial_capital" : 5.0, "period" : 3, "capitalKey" : "capital", "portfolioValueKey" : "portfolio_value","target":"target",
                              "feesDict" : {0:0, -1:-1, 1:1}, "positionFees" : "positionFees",'pnl': 'pnl', 'instrumentId1':'instrumentId1', 'instrumentId2':'instrumentId2', 'featureName': 'featureName', "predictionKey": "predictionKey",
                              "dict1":{'maxPortfolioValue': "asdas" , 'maxDrawdown': "asdas"}, "dict2":{'maxPortfolioValue': "asda" , 'maxDrawdown': "asda"}, "instrument_pnl_feature" : 'pnlKey',"pnlKey" : "pnlKey","instrument_score_feature": "score"}
            return {"data" : data, "featureParams" : featureParams, 'cap'   :   6.0,
                                                                    'capM'  :   -3.0,
                                                                    'fees'  :   [3.0],
                                                                    'pos'   :   {0.0: 4, 2.0: 4},
                                                                    'port'  :   9.0,
                                                                    'ci'    :   0,
                                                                    'maxc'  :   8.0 ,
                                                                    'scorer':   1.08,
                                                                    'plm'   :   1.25,
                                                                    'pli'   :   [0.0],
                                                                    'vari'  :   [2.79],
                                                                    'varm'  :   [0.54],
                                                                    'totpi' :   [4.25],
                                                                    'totpm' :   [1.25],
                                                                    'totli' :   [3.0],
                                                                    'totlm' :   [0.0],
                                                                    'cntpi' :   [4.0],
                                                                    'cntpm' :   [1.0],
                                                                    'cntli' :   [3.0],
                                                                    'cntlm' :   [0.0],
                                                                    'scrfi' :   [2.9],
                                                                    'scrfm' :   [5.42],
                                                                    'scrli' :   [2.82],
                                                                    'scrlm' :   [5.42],
                                                                    'maxd'  :   {'maxDrawdown': 10.01, 'maxPortfolioValue': 5.85}}
