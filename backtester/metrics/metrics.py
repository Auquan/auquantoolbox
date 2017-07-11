import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

class Metrics():
    def __init__(self, marketFeaturesDf):
        self.__marketFeaturesDf = marketFeaturesDf
        self.__stats = {}

    def getMetricsString(self):
        return 'Total Pnl: %0.2f%%'%self.__stats['Total Pnl(%)'] + '\t' + \
        'Ann. Return: %0.2f%%'%self.__stats['Annual Return(%)'] + '\t' + \
        'Ann. Vol: %0.2f%%'%self.__stats['Annual Vol(%)'] + '\t' + \
        'Base Return: %0.2f%%'%self.__stats['Base Return(%)'] + '\t' + \
        'Sharpe Ratio: %0.2f'%self.__stats['Sharpe Ratio'] + '\t' + \
        'Sortino Ratio: %0.2f'%self.__stats['Sortino Ratio'] + '\t' + \
        'Max Drawdown: %0.2f%%'%self.__stats['Max Drawdown(%)'] + '\t' + \
        'Profit/Loss Ratio: %0.2f'%self.__stats['Profit/Loss Ratio'] + '\t' + \
        'Accuracy: %0.2f%%'%self.__stats['Accuracy'] + '\t' 
        #+ 'Log Loss         : %0.2f'%self.__stats['Log Loss'] 

    def getMetrics(self):
        return self.__stats

    def calculateMetrics(self, baseSymbol, priceFeature, folderName):

        stats = {}
        total_pnl = self.__marketFeaturesDf['pnl']
        portfolioValue = self.__marketFeaturesDf['portfolio_value']
        total_days = len(total_pnl)
        total_return = total_pnl[total_days-1]/portfolioValue[0]
        
        daily_return = portfolioValue /portfolioValue.shift(1) - 1
        daily_return.dropna(inplace=True)
        #prediction = self.__marketFeaturesDf['prediction']
        benchmark = self.getBenchmarkData(baseSymbol,priceFeature, folderName)

        stats['Total Pnl(%)'] = total_return
        stats['Annual Return(%)'] = self.annualized_return(total_return, total_days)
        stats['Base Return(%)'] = self.annualized_return(benchmark['total_returns'],total_days)
        stats['Annual Vol(%)']= self.annual_vol(daily_return)
        #stats['Beta'] = self.beta(daily_return,benchmark['daily_returns'])
        stats['Sharpe Ratio'] = self.sharpe_ratio(total_return, total_days, daily_return)
        stats['Sortino Ratio'] = self.sortino_ratio(total_return, total_days, daily_return)
        stats['Max Drawdown(%)'] = self.max_drawdown(portfolioValue)
        stats['Profit/Loss Ratio']= self.profit_factor(daily_return)
        stats['Accuracy']=self.accuracy(daily_return)
        #stats['Log Loss']=logLoss(daily_return)

        self.__stats = stats

    def annualized_return(self, total_return, total_days):
        return 100*((1 + total_return)**(252 / total_days) - 1)
        

    def annualized_std(self, daily_return):
        return np.sqrt(252)*np.std(daily_return)

    def annualized_downside_std(self, daily_return):
        mar = 0
        downside_return = daily_return.copy()
        downside_return[downside_return > 0]= 0
        return np.sqrt(252)*np.std(downside_return)

    def annual_vol(self, daily_return):
        return self.annualized_std(daily_return)

    def sharpe_ratio(self, total_return, total_days, daily_return):
        stdev = self.annualized_std(daily_return)
        if stdev == 0:
            return np.nan
        else:
            return self.annualized_return(total_return, total_days)/stdev

    def sortino_ratio(self, total_return, total_days, daily_return):
        stdev = self.annualized_downside_std(daily_return)
        if stdev == 0:
            return np.nan
        else:
            return self.annualized_return(total_return, total_days)/stdev

    def max_drawdown(self, portfolioValue):
        return np.max(np.maximum.accumulate(portfolioValue) - portfolioValue)/portfolioValue[0]

    def beta(self, daily_return, baseline_daily_return):
        stdev = np.std(baseline_daily_return)
        print(len(daily_return), len(baseline_daily_return))
        if stdev == 0:
            return np.nan
        else:
            return np.corrcoef(daily_return, baseline_daily_return)[0,1]*np.std(daily_return)/stdev

    def alpha(self, daily_return, baseline_daily_return,beta):
        return self.annualized_return(daily_return) - beta*self.annualized_return(baseline_daily_return)

    def profit_factor(self,daily_return):
        downside_return = daily_return.copy()
        downside_return[downside_return > 0]= 0
        upside_return = daily_return.copy()
        upside_return[upside_return < 0]= 0
        if downside_return.sum() == 0:
            return 0
        return -(upside_return.sum())/(downside_return.sum())

    def accuracy(self,daily_return):
        total_return = daily_return.copy()
        total_return[total_return != 0]= 1
        upside_return = daily_return.copy()
        upside_return[upside_return < 0]= 0
        upside_return[upside_return > 0]= 1
        if total_return.sum() == 0:
            return 0
        return upside_return.sum()/total_return.sum()

    def getBenchmarkData(self,baseSymbol,priceFeature, folderName):
        baseline_data = {}
        path = folderName + '/' + baseSymbol + '_features.csv'
        csv = pd.read_csv(path, engine='python')
        #features = [col.upper() for col in csv.columns]
        baseline_data['price'] =  csv[priceFeature]
        start = baseline_data['price'][0]
        last = baseline_data['price'][len(baseline_data['price'])-1]
        baseline_data['total_returns'] = last/start - 1
        baseline_data['daily_returns'] =  baseline_data['price']/baseline_data['price'].shift(1) - 1
        baseline_data['daily_returns'].dropna(inplace=True)
        return baseline_data            