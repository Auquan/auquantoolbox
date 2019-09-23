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
		
		str = ''
		for key, val in self.__stats.items():
			str += \
				' %s: %0.2f '%(key, val) 
		# str = \
		# 	' Total Pnl: %0.2f%% ' % (100 * self.__stats['pnl']) \
		# 	+ ' Max Drawdown: %0.2f%% ' % (100 * self.__stats['maxDrawdown']) \
		# 	+ ' RoC: %0.2f%% ' % (100 * self.__stats['roc']) \
		# 	+ ' P/L Ratio: %0.2f ' % self.__stats['pl_ratio']
		# if 'accuracy' in self.__stats.keys():
		# 	str += ' Trade Accuracy: %0.2f ' % self.__stats['accuracy']
		# if 'score' in self.__stats:
		# 	str = str + ' Score: %0.2f ' % self.__stats['score']
		# if self.__stats['trading_days'] > 252:
		# 	str = str \
		# 		+ ' Ann. Return: %0.2f%% ' % (100 * self.__stats['annual_return']) \
		# 		+ ' Ann. Vol: %0.2f%% ' % (100 * self.__stats['annual_vol']) \
		# 		+ ' Sharpe Ratio: %0.2f ' % self.__stats['sharpe_ratio']

		return str

	def getInstrumentMetricsString(self):
		# Add back below once benchmark support
		# + ' Benchmark: %0.2f%% ' % (100 * self.__stats['Base Return(%)']) \
		str = \
			' Pnl: %0.2f ' % self.__stats['pnl'] \
			+ ' Profit/Loss Ratio: %0.2f ' % self.__stats['pl_ratio'] \
			+ ' Trade Accuracy: %0.2f ' % self.__stats['accuracy']
		if 'score' in self.__stats:
			str = str + ' Score: %0.2f ' % self.__stats['score']
		if 'normalized_score' in self.__stats:
			str = str + ' Normalized Score: %0.2f ' % self.__stats['normalized_score']
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

	
	def getMarketStats(self, marketFeaturesDf, startingCapital, metrics_to_show=None, dateBounds=None, priceFeature=None):
		df = marketFeaturesDf
		if metrics_to_show is None:
			metrics_to_show = df.columns

		stats = {}
		total_return = df['pnl'].iloc[- 1] / float(startingCapital)
		if 'pnl' in metrics_to_show:
			stats['pnl'] = total_return
		if 'roc' in metrics_to_show:
			stats['roc'] = self.roc(df['pnl'].iloc[- 1], df['capitalUsage'].iloc[-1])
		if 'max_drawdown' in metrics_to_show:
			stats['max_drawdown'] = self.max_drawdown(df['maxDrawdown'].iloc[-1], startingCapital)
		if 'pl_ratio' in metrics_to_show:
			stats['pl_ratio'] = self.profit_factor(df['total_profit'].iloc[-1], df['total_loss'].iloc[-1])
		if 'accuracy' in metrics_to_show:
			stats['accuracy'] = self.accuracy(df['count_profit'].iloc[-1], df['count_loss'].iloc[-1])

		if dateBounds is not None:
			benchmark = self.getBenchmarkData(None, priceFeature, '')
			print(dateBounds)
			total_days = len(pd.date_range(dateBounds[0], dateBounds[1], freq=BDay()))
			stats['trading_days'] = total_days
			if total_days > 252:
				stats['annual_return'] = self.annualized_return(total_return, total_days)
				if benchmark is not None:
					stats['base_return'] = self.annualized_return(
						benchmark['total_return'], total_days)
				stats['annual_vol'] = self.annual_vol(df['variance'].iloc[-1], startingCapital)
				stats['sharpe_ratio'] = self.sharpe_ratio(stats['annual_return'], stats['annual_vol'])

		if 'score' in df.columns:
			stats['score'] = df['score'].iloc[-1]

		metrics_set = set(metrics_to_show) - set(list(stats.keys()))
		for metric in metrics_set:
			try:
				if metric == 'maxDrawdown':
					stats['maxDrawdown'] = df[metric][-1]['maxDrawdown']
					stats['maxPortfolioValue'] = df[metric][-1]['maxPortfolioValue']
				else:
					stats[metric] = df[metric][-1]
			except Exception as e:
				print('Could not log the metric: %s'%metric)
				print(e)
	
		return stats

	def getInstrumentStats(self, instrumentLookbackData, startingCapital, instrumentIds, metrics_to_show = None):
		
		if metrics_to_show is None:
			metrics_to_show = instrumentLookbackData.getAllFeatures()
		
		pnl = instrumentLookbackData.getFeatureDf('pnl').iloc[-1]
		total_profit = instrumentLookbackData.getFeatureDf('total_profit').iloc[-1]
		total_loss = instrumentLookbackData.getFeatureDf('total_loss').iloc[-1]
		count_profit = instrumentLookbackData.getFeatureDf('count_profit').iloc[-1]
		count_loss = instrumentLookbackData.getFeatureDf('count_loss').iloc[-1]
		totalReturn = pnl / float(startingCapital)
		stats = {}

		for instrumentId in instrumentIds:
			if 'pnl' in metrics_to_show:
				if 'pnl' not in stats.keys():
					stats['pnl'] = {}
				stats['pnl'][instrumentId] = totalReturn.loc[instrumentId]
			if 'pl_ratio' in metrics_to_show:
				if 'pl_ratio' not in stats.keys():
					stats['pl_ratio'] = {}
				stats['pl_ratio'][instrumentId] = self.profit_factor(total_profit.loc[instrumentId], total_loss.loc[instrumentId])
			if 'accuracy' in metrics_to_show:
				if 'accuracy' not in stats.keys():
					stats['accuracy'] = {}
				stats['accuracy'][instrumentId] = self.accuracy(count_profit.loc[instrumentId], count_loss.loc[instrumentId])
			try:
				if 'score' in metrics_to_show:
					if 'score' not in stats.keys():
						stats['score'] = {}
					score = instrumentLookbackData.getFeatureDf('score').iloc[-1]
					stats['score'][instrumentId] = score.loc[instrumentId]
				try:
					if 'normalized_score' in metrics_to_show:
						if 'normalized_score' not in stats.keys():
							stats['normalized_score'] = {}
						benchmarkScore = instrumentLookbackData.getFeatureDf('benchmark_score').iloc[-1]
						stats['normalized_score'][instrumentId] = 1000 * score.loc[instrumentId] / benchmarkScore.loc[instrumentId]
				except KeyError:
					pass
			except KeyError:
				pass

		metrics_set = set(metrics_to_show) - set(list(stats.keys()))
		for metric in metrics_set:
			try:
				stats[metric] = {}
				for instrumentId in instrumentIds:
					val = instrumentLookbackData.getFeatureDf(metric).iloc[-1]
					stats[metric][instrumentId] = val.loc[instrumentId]
			except Exception as e:
				print('Could not log the metric: %s'%metric)
				print(e)

		return stats

	def calculateMarketMetricsRealtime(self, marketFeaturesDf, startingCapital, metrics_to_show=None):
		if metrics_to_show is None:
			metrics_to_show = set(marketFeaturesDf.columns)
		
		diff = set(metrics_to_show) - set(marketFeaturesDf.columns)
		if len( diff ) > 0:
			print('Some of the market metrics you asked for are not available!!')
			print('Available metrics: %s'%marketFeaturesDf.columns)
			print('Following are not available: %s'%diff)
		
		stats = self.getMarketStats(marketFeaturesDf, startingCapital, metrics_to_show=metrics_to_show)
		return stats

	def calculateMarketMetrics(self, priceFeature, startingCapital, dateBounds):
		stats = self.getMarketStats(self.__marketFeaturesDf, startingCapital, dateBounds=dateBounds, priceFeature=priceFeature)
		self.__stats = stats

	def calculateInstrumentFeatureMetricsRealtime(self, instrumentIds, instrumentLookbackData, startingCapital, metrics_to_show=None):
		
		if metrics_to_show is None:
			metrics_to_show = instrumentLookbackData.getAllFeatures()

		diff = set(metrics_to_show) - set(instrumentLookbackData.getAllFeatures())
		if len( diff ) > 0:
			print('Some of the instrument metrics you asked for are not available!!')
			print('Available metrics: %s'%instrumentLookbackData.getAllFeatures())
			print('Following are not available: %s'%diff)

		stats = self.getInstrumentStats(instrumentLookbackData, startingCapital, instrumentIds, metrics_to_show)
		return stats

	def calculateInstrumentFeatureMetrics(self, instrumentId, priceFeature, startingCapital, instrumentLookbackData):
		self.__stats = self.getInstrumentStats(instrumentLookbackData, startingCapital, [instrumentId])

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
