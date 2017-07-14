import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
from functools import partial
from pandas.tseries.frequencies import to_offset

class Metrics():
    def __init__(self, marketFeaturesDf):
        self.__marketFeaturesDf = marketFeaturesDf
        self.__stats = {}

    def getMarketMetricsString(self):
        return \
          ' Total Pnl: %0.2f%% '%(100*self.__stats['Total Pnl(%)']) \
        + ' Ann. Return: %0.2f%% '%(100*self.__stats['Annual Return(%)']) \
        + ' Ann. Vol: %0.2f%% '%(100*self.__stats['Annual Vol(%)']) \
        + ' Benchmark: %0.2f%% '%(100*self.__stats['Base Return(%)']) \
        + ' Sharpe Ratio: %0.2f '%self.__stats['Sharpe Ratio'] \
        + ' Sortino Ratio: %0.2f '%self.__stats['Sortino Ratio'] \
        + ' Max Drawdown: %0.2f%% '%(100*self.__stats['Max Drawdown(%)']) \
        + ' Profit/Loss Ratio: %0.2f '%self.__stats['Profit/Loss Ratio'] \
        + ' Accuracy: %0.2f%% '%self.__stats['Accuracy'] 
        #+ 'Log Loss         : %0.2f'%self.__stats['Log Loss'] 

    def getMetricsString(self):
        return \
          ' Total Pnl: %0.2f '%(self.__stats['Total Pnl(%)']) \
        + ' Benchmark: %0.2f%% '%self.__stats['Base Return(%)'] \
        + ' Profit/Loss Ratio: %0.2f '%self.__stats['Profit/Loss Ratio'] \
        + ' Accuracy: %0.2f%% '%self.__stats['Accuracy'] 
        #+ 'Log Loss         : %0.2f'%self.__stats['Log Loss'] 

    def getMetrics(self):
        return self.__stats

    def round(self, t, freq):
        freq = to_offset(freq)
        return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)

    def resampleData(self, series, period):
        return series.groupby(partial(self.round, freq=period))
        #series.resample(period)

    def calculateMarketMetrics(self, baseSymbol, priceFeature, startingCapital, folderName):

        stats = {}
        
        total_pnl = self.resampleData(self.__marketFeaturesDf['pnl'], '1D').last()
        portfolioValue = self.resampleData(self.__marketFeaturesDf['portfolio_value'], '1D').last()
        total_days = len(total_pnl)
        total_return = total_pnl[total_days-1]/startingCapital        
        daily_return = (portfolioValue /portfolioValue.shift(1) - 1)
        daily_return.dropna(inplace=True)
        #prediction = self.__marketFeaturesDf['prediction']
        benchmark = self.getBenchmarkData(baseSymbol,priceFeature, folderName)
        
        stats['Total Pnl(%)'] = total_return
        stats['Annual Return(%)'] = self.annualized_return(total_return, total_days)
        stats['Base Return(%)'] = self.annualized_return(benchmark['total_return'],total_days)
        stats['Annual Vol(%)']= self.annual_vol(daily_return)
        #stats['Beta'] = self.beta(daily_return,benchmark['daily_returns'])
        stats['Sharpe Ratio'] = self.sharpe_ratio(total_return, total_days, daily_return)
        stats['Sortino Ratio'] = self.sortino_ratio(total_return, total_days, daily_return)
        stats['Max Drawdown(%)'] = self.max_drawdown(self.__marketFeaturesDf['portfolio_value'])
        stats['Profit/Loss Ratio']= self.profit_factor(total_pnl)
        stats['Accuracy']=self.accuracy(self.__marketFeaturesDf['pnl'])
        #stats['Log Loss']=logLoss(daily_return)
        print(stats)
        self.__stats = stats

    def calculateMetrics(self, priceFeature, startingCapital):

        stats = {}
        
        total_pnl = self.resampleData(self.__marketFeaturesDf['pnl'], '1D').last()
        price = self.resampleData(self.__marketFeaturesDf[priceFeature], '1D').last()
        total_days = len(total_pnl)
        total_return = total_pnl[total_days-1]/startingCapital
        base_return = price[total_days-1]/price[0] - 1
        daily_return = price /price.shift(1) - 1
        daily_return.dropna(inplace=True)

        stats['Total Pnl(%)'] = total_return
        stats['Base Return(%)'] = self.annualized_return(base_return,total_days)
        stats['Profit/Loss Ratio']= self.profit_factor(total_pnl)
        stats['Accuracy']=self.accuracy(self.__marketFeaturesDf['pnl'])
        #stats['Log Loss']=logLoss(daily_return)
        print(stats)
        self.__stats = stats

    def annualized_return(self, total_return, total_days):
        annualized_return = ((1 + total_return)**(252.0/np.float(total_days)) - 1)
        return annualized_return
        

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
        if stdev == 0:
            return np.nan
        else:
            return np.corrcoef(daily_return, baseline_daily_return)[0,1]*np.std(daily_return)/stdev

    def alpha(self, daily_return, baseline_daily_return,beta):
        return self.annualized_return(daily_return) - beta*self.annualized_return(baseline_daily_return)

    def profit_factor(self,daily_return):
        returns = (daily_return-daily_return.shift(1))
        returns.dropna(inplace=True)
        downside_return = returns.copy()
        downside_return[downside_return > 0]= 0
        upside_return = returns.copy()
        upside_return[upside_return < 0]= 0
        if downside_return.sum() == 0:
            return 0
        return -(upside_return.sum())/(downside_return.sum())

    def accuracy(self,daily_return):
        returns = (daily_return-daily_return.shift(1))
        returns.dropna(inplace=True)
        total_return = returns.copy()
        total_return[total_return != 0]= 1
        upside_return = returns.copy()
        upside_return[upside_return < 0]= 0
        upside_return[upside_return > 0]= 1
        if total_return.sum() == 0:
            return 0
        return upside_return.sum()/total_return.sum()

    def getBenchmarkData(self,baseSymbol,priceFeature, folderName):
        baseline_data = {}
        path = folderName + '/' + baseSymbol + '_features.csv'
        csv = pd.read_csv(path, engine='python')
        csv.set_index(csv['time'], inplace=True)
        csv.index = pd.to_datetime(csv.index)
        #features = [col.upper() for col in csv.columns]
        baseline_data['price'] =  self.resampleData(csv[priceFeature], '1D').last()
        start = baseline_data['price'][0]
        baseline_data['returns'] = baseline_data['price']/start - 1
        baseline_data['total_return'] = baseline_data['returns'][len(baseline_data['price'])-1]
        baseline_data['daily_returns'] =  baseline_data['price']/baseline_data['price'].shift(1) - 1
        baseline_data['daily_returns'].dropna(inplace=True)
        return baseline_data            