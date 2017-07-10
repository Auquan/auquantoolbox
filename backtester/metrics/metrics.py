import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

class Metrics():
    def __init__(self, parentFolderName, runName):
        self.__runName = runName
        self.__folderName = parentFolderName + '/' + 'runLog_' + runName
        self.__marketFeaturesDf = self.__folderName + '/marketFeatures.csv'
        self.__stats = {}

    def getCumulativeReturns(self):
        return self.__cumulativePnl

    def getMetrics(self):
        return self.__stats

    def calculateMetrics(cumulativePnl, baseData):

        stats = {}
        daily_return = daily_pnl.sum(axis=1)
        total_return = total_pnl.sum(axis=1)

        stats['Total Pnl(%)'] = (total_pnl.iloc[total_pnl.index.size-1].sum())
        stats['Annual Return(%)'] = self.annualized_return(daily_return)
        stats['Base Return(%)'] = self.annualized_return(baseline_data['DAILY_PNL'])
        stats['Annual Vol(%)']= self.annual_vol(daily_return)
        stats['Beta'] = self.beta(daily_return,baseline_data['DAILY_PNL'])
        stats['Sharpe Ratio'] = self.sharpe_ratio(daily_return)
        stats['Sortino Ratio'] = self.sortino_ratio(daily_return)
        stats['Max Drawdown(%)'] = self.max_drawdown(daily_return)
        stats['Profit/Loss Ratio']= self.profit_factor(daily_return)
        stats['Accuracy']=profit_percent(daily_return)
        stats['Log Loss']=logLoss(daily_return)
            # stats = 'Total Pnl        : %0.2f'%(total_pnl.iloc[total_pnl.index.size-1].sum()) + '\t' + \
            #         'Annualized Return: %0.2f%%'%annualized_return(daily_return) + '\t' + \
            #         'Benchmark Return : %0.2f%%'%annualized_return(baseline_data['DAILY_PNL']) + '\t' + \
            #         'Annual Vol       : %0.2f%%'%annual_vol(daily_return) + '\t' + \
            #         'Beta             : %0.2f'%beta(daily_return,baseline_data['DAILY_PNL']) + '\t' + \
            #         'Sharpe Ratio     : %0.2f'%sharpe_ratio(daily_return) + '\t' + \
            #         'Sortino Ratio    : %0.2f'%sortino_ratio(daily_return) + '\t' + \
            #         'Max Drawdown     : %0.2f'%max_drawdown(daily_return)
    self.__stats = stats

    def annualized_return(cumulativePnl):
        total_return = daily_return.sum()/100
        total_days = daily_return.index.size
        return 100*((1 + total_return)**(252 / total_days) - 1)
        

    def annualized_std(daily_return):
        return np.sqrt(252)*np.std(daily_return)

    def annualized_downside_std(daily_return):
        mar = 0
        downside_return = daily_return.copy()
        downside_return[downside_return > 0]= 0
        return np.sqrt(252)*np.std(downside_return)

    def annual_vol(daily_return):
        return annualized_std(daily_return)

    def sharpe_ratio(daily_return):
        stdev = annualized_std(daily_return)
        if stdev == 0:
            return np.nan
        else:
            return annualized_return(daily_return)/stdev

    def sortino_ratio(daily_return):
        stdev = annualized_downside_std(daily_return)
        if stdev == 0:
            return np.nan
        else:
            return annualized_return(daily_return)/stdev

    def max_drawdown(daily_return):
        return np.max(np.maximum.accumulate(daily_return) - daily_return)

    def beta(daily_return, baseline_daily_return):
        stdev = np.std(baseline_daily_return)
        if stdev == 0:
            return np.nan
        else:
            return np.corrcoef(daily_return, baseline_daily_return)[0,1]*np.std(daily_return)/stdev

    def alpha(daily_return, baseline_daily_return,beta):
        return annualized_return(daily_return) - beta*annualized_return(baseline_daily_return)

    def profit_factor(daily_return):
        downside_return = daily_return.copy()
        downside_return[downside_return > 0]= 0
        upside_return = daily_return.copy()
        upside_return[upside_return < 0]= 0
        if downside_return.sum() == 0:
            return 0
        return -(upside_return.sum())/(downside_return.sum())

    def accuracy(daily_return):
        total_return = daily_return.copy()
        total_return[total_return != 0]= 1
        upside_return = daily_return.copy()
        upside_return[upside_return < 0]= 0
        upside_return[upside_return > 0]= 1
        if total_return.sum() == 0:
            return 0
        return upside_return.sum()/total_return.sum()

    def baseline(baseSymbol,priceFeature):
        baseline_data = {}
        path = self.__folderName + '/' + baseSymbol + '_features.csv'
        csv = pd.read_csv(path)
        csv.index = pd.to_datetime(csv.index)
        csv = csv.reindex(index=csv.index[::-1])
        #features = [col.upper() for col in csv.columns]

        baseline_data['price'] =  csv[priceFeature]
        start = baseline_data['price'][0]
        baseline_data['total_returns'] = baseline_data['price']/start
        baseline_data['daily_returns'] =  baseline_data['total_returns'] /baseline_data['total_returns'].shift(1) - 1
        baseline_data.dropna(inplace=True)
        return baseline_data            