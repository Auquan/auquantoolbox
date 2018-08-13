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
        # TODO add the snippet back once benchmark is fixed.
        # + ' Benchmark: %0.2f%% ' % (100 * self.__stats['Base Return(%)']) \
        str = \
            ' Total Pnl: %0.2f%% ' % (100 * self.__stats['Total Pnl(%)']) \
            + ' Max Drawdown: %0.2f%% ' % (100 * self.__stats['Max Drawdown(%)']) \
            + ' RoC: %0.2f%% ' % (100 * self.__stats['RoC(%)']) \
            + ' P/L Ratio: %0.2f ' % self.__stats['Profit/Loss Ratio'] \
            + ' Trade Accuracy: %0.2f ' % self.__stats['Accuracy']
        if 'Score' in self.__stats:
            str = str + ' Score: %0.2f ' % self.__stats['Score']
        if self.__stats['Trading Days'] > 252:
            str = str \
                + ' Ann. Return: %0.2f%% ' % (100 * self.__stats['Annual Return(%)']) \
                + ' Ann. Vol: %0.2f%% ' % (100 * self.__stats['Annual Vol(%)']) \
                + ' Sharpe Ratio: %0.2f ' % self.__stats['Sharpe Ratio']

        return str

    def getInstrumentMetricsString(self):
        # Add back below once benchmark support
        # + ' Benchmark: %0.2f%% ' % (100 * self.__stats['Base Return(%)']) \
        str = \
            ' Pnl: %0.2f ' % self.__stats['Pnl'] \
            + ' Total Pnl: %0.2f%% ' % (100 * self.__stats['Total Pnl(%)']) \
            + ' Profit/Loss Ratio: %0.2f ' % self.__stats['Profit/Loss Ratio'] \
            + ' Trade Accuracy: %0.2f ' % self.__stats['Accuracy']
        if 'Score' in self.__stats:
            str = str + ' Score: %0.2f ' % self.__stats['Score']
        if 'Normalized Score' in self.__stats:
            str = str + ' Normalized Score: %0.2f ' % self.__stats['Normalized Score']
        return str

    def getMetrics(self):
        return self.__stats

    def getDf(self):
        return self.__marketFeaturesDf

    def round(self, t, freq):
        freq = to_offset(freq)
        return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)

    def resampleData(self, series, period):
        return series.groupby(partial(self.round, freq=period))
        # series.resample(period)

    def calculateMarketMetrics(self, baseSymbol, priceFeature, startingCapital, dateBounds):

        stats = {}
        df = self.__marketFeaturesDf

        # total_pnl = self.resampleData(
        #     self.__marketFeaturesDf['pnl'], '1D').last()  # TODO change 'pnl'
        # portfolioValue = self.resampleData(
        #     self.__marketFeaturesDf['portfolio_value'], '1D').last()  # TODO change portfolio_value
        # total_pnl.dropna(inplace=True)
        # portfolioValue.dropna(inplace=True)
        total_days = len(pd.date_range(dateBounds[0], dateBounds[1], freq=BDay()))
        total_return = df['pnl'].iloc[- 1] / float(startingCapital)

        benchmark = self.getBenchmarkData(None, priceFeature, '')
        stats['Trading Days'] = total_days
        stats['Total Pnl(%)'] = total_return
        stats['RoC(%)'] = self.roc(df['pnl'].iloc[- 1], df['capitalUsage'].iloc[-1])
        stats['Max Drawdown(%)'] = self.max_drawdown(df['maxDrawdown'].iloc[-1], startingCapital)
        stats['Profit/Loss Ratio'] = self.profit_factor(df['total_profit'].iloc[-1], df['total_loss'].iloc[-1])
        stats['Accuracy'] = self.accuracy(df['count_profit'].iloc[-1], df['count_loss'].iloc[-1])
        if total_days > 252:
            stats['Annual Return(%)'] = self.annualized_return(
                total_return, total_days)
            if benchmark is not None:
                stats['Base Return(%)'] = self.annualized_return(
                    benchmark['total_return'], total_days)
            stats['Annual Vol(%)'] = self.annual_vol(df['variance'].iloc[-1], startingCapital)
            stats['Sharpe Ratio'] = self.sharpe_ratio(stats['Annual Return(%)'], stats['Annual Vol(%)'])

        # TODO change reference to score
        if 'score' in df.columns:
            stats['Score'] = df['score'].iloc[-1]
        self.__stats = stats

    def calculateInstrumentFeatureMetrics(self, instrumentId, priceFeature, startingCapital, instrumentLookbackData):
        stats = {}
        pnl = instrumentLookbackData.getFeatureDf('pnl').iloc[-1]
        total_profit = instrumentLookbackData.getFeatureDf('total_profit').iloc[-1]
        total_loss = instrumentLookbackData.getFeatureDf('total_loss').iloc[-1]
        count_profit = instrumentLookbackData.getFeatureDf('count_profit').iloc[-1]
        count_loss = instrumentLookbackData.getFeatureDf('count_loss').iloc[-1]

        totalReturn = pnl / float(startingCapital)
        stats['Pnl'] = pnl.loc[instrumentId]
        stats['Total Pnl(%)'] = totalReturn.loc[instrumentId]
        stats['Profit/Loss Ratio'] = self.profit_factor(total_profit.loc[instrumentId], total_loss.loc[instrumentId])
        stats['Accuracy'] = self.accuracy(count_profit.loc[instrumentId], count_loss.loc[instrumentId])
        try:
            score = instrumentLookbackData.getFeatureDf('score').iloc[-1]
            stats['Score'] = score.loc[instrumentId]
            try:
                benchmarkScore = instrumentLookbackData.getFeatureDf('benchmark_score').iloc[-1]
                stats['Normalized Score'] = 1000 * score.loc[instrumentId] / benchmarkScore.loc[instrumentId]
            except KeyError:
                pass
        except KeyError:
            pass

        self.__stats = stats

    def annualized_return(self, total_return, total_days):
        annualized_return = ((1 + total_return) **
                             (252.0 / np.float(total_days)) - 1)

        return annualized_return

    def annualized_std(self, variance, startingCapital):
        return (np.sqrt(252) * np.sqrt(variance)) / float(startingCapital)

    def annualized_downside_std(self, daily_return):
        downside_return = daily_return.copy()
        downside_return[downside_return > 0] = 0
        return np.sqrt(252) * np.std(downside_return)

    def annual_vol(self, variance, startingCapital):
        return self.annualized_std(variance, startingCapital)

    def sharpe_ratio(self, annual_return, annual_vol):
        if annual_vol == 0:
            return np.nan
        else:
            return annual_return / float(annual_vol)

    def sortino_ratio(self, total_return, total_days, daily_return):
        stdev = self.annualized_downside_std(daily_return)
        if stdev == 0:
            return np.nan
        else:
            return self.annualized_return(total_return, total_days) / stdev

    def max_drawdown(self, maxDrawdown, startingCapital):
        return maxDrawdown['maxDrawdown'] / float(startingCapital)
        # return np.max(np.maximum.accumulate(portfolioValue) - portfolioValue) / portfolioValue[0]

    def roc(self, total_pnl, capitalUsage):
        if capitalUsage > 0:
            return total_pnl / float(capitalUsage)
        else:
            return np.nan

    def beta(self, daily_return, baseline_daily_return):
        stdev = np.std(baseline_daily_return)
        if stdev == 0:
            return np.nan
        else:
            return np.corrcoef(daily_return, baseline_daily_return)[0, 1] * np.std(daily_return) / stdev

    def alpha(self, daily_return, baseline_daily_return, beta):
        return self.annualized_return(daily_return) - beta * self.annualized_return(baseline_daily_return)

    def profit_factor(self, total_profit, total_loss):
        if total_loss == 0:
            return float('nan')
        return total_profit / float(total_loss)

    def profitability(self, total_profit, total_pnl):
        if total_pnl == 0:
            return 0
        return total_profit / float(total_pnl)

    def profit_factor_avg(self, total_profit, total_loss, count_profit, count_loss):
        if total_loss == 0 or count_loss == 0:
            return float('nan')
        return (total_profit / float(count_profit))\
            / (total_loss / float(count_loss))

    def accuracy(self, count_profit, count_loss):
        total_count = count_profit + count_loss
        if total_count == 0:
            return 0
        return count_profit / float(total_count)

    def getBenchmarkData(self, baseSymbol, priceFeature, folderName):
        if (baseSymbol is None):
            return None

        baseline_data = {}
        path = folderName + '/' + baseSymbol + '_features.csv'
        csv = pd.read_csv(path, engine='python')
        csv.set_index(csv['time'], inplace=True)
        csv.index = pd.to_datetime(csv.index)
        # features = [col.upper() for col in csv.columns]
        baseline_data['price'] = self.resampleData(
            csv[priceFeature], '1D').last()
        start = baseline_data['price'][0]
        baseline_data['returns'] = baseline_data['price'] / start - 1
        baseline_data['total_return'] = baseline_data['returns'][len(
            baseline_data['price']) - 1]
        baseline_data['daily_returns'] = baseline_data['price'] / \
            baseline_data['price'].shift(1) - 1
        baseline_data['daily_returns'].dropna(inplace=True)
        return baseline_data
