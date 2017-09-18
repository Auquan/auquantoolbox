import pandas as pd
import numpy as np
from backtester.plotter import generateGraph
from os import listdir
from os.path import isfile, join, basename
from backtester.metrics.metrics import Metrics
from backtester.logger import *
from pandas.tseries.frequencies import to_offset
from functools import partial

'''
Usage(to test in console):
>> pip install plotly
>> python
>> from plotter import plot
>> plot(r'./runLogs/runLog_20170613_201741', []) # plots every file in directory
>> plot(r'./runLogs/runLog_20170613_201741', ['ADBE_features.csv']) # ignores the files listed here
>> plot(r'./runLogs/runLog_20170613_201741/ADBE_features.csv', []) # plots only ADBE_features
Replace the appropriate timeStamps

TODO: 1) Support excluding columns for each files.
      2) Cleanup the html files generated from plotting/dont regenerate and recycle ones present.
      3) Provide a selector GUI to chose the files.
'''


def processResult(dir, marketFeatures, benchmark, stats, metricString, startingCapital, excludeFiles, shouldPlot):
    resultDict = {}
    if marketFeatures is not None and isfile(marketFeatures):
        df, benchmark_pnl = getDataReady(
            dir, marketFeatures, benchmark, startingCapital, True)
        if shouldPlot:
            logInfo('Generating %s' % marketFeatures)
            generateGraph(df, marketFeatures, metricString, benchmark_pnl)
        resultDict['metrics'] = stats.keys()
        resultDict['metrics_values'] = stats.values()
        resultDict['score'] = stats['Score']
        sampledDf = resampleData(df['pnl'], '1H').last()

        resultDict['dates'] = sampledDf.index.values
        resultDict['total_pnl'] = sampledDf.values
    else:
        resultDict['instrument_names'] = []
        resultDict['instrument_stats'] = []
        for fileName in listdir(dir):
            path = dir + '/' + fileName
            if (not isfile(path)) or (path in excludeFiles) or (fileName in excludeFiles):
                logInfo('excluding ', fileName)
                continue
            logInfo('Generating %s' % fileName)
            df, benchmark_pnl = getDataReady(
                dir, path, benchmark, startingCapital, False)
            if shouldPlot:
                logInfo('Generating %s' % fileName)
                generateGraph(df, path, fileName + ' ' + metricString, benchmark_pnl)
            resultDict['instrument_names'] += [fileName.split('_')[0]]
            resultDict['instrument_stats'] += [{'total_pnl': stats['Total Pnl(%)'], 'score': stats['Score']}]
    return resultDict

def getDataReady(dir, features, benchmark, startingCapital, market=True):
    df = pd.read_csv(features, engine='python',
                     index_col='time', parse_dates=True)
    if market:
        df['Returns(%)'] = 100 * (df['pnl'] / startingCapital)
        # metrics = Metrics(marketFeaturesDf=df)
        # metrics.calculateMarketMetrics(benchmark, price, startingCapital, dir)
        # # TODO create benchamrks later
        benchmark_pnl = None
    else:
        # metrics = Metrics(marketFeaturesDf=df)
        # metrics.calculateMetrics(price, startingCapital)
        benchmark_pnl = None
    # logInfo(stats, True)
    return df, benchmark_pnl

def resampleData(series, period):
    return series.groupby(partial(round, freq=period))

def round(t, freq):
    freq = to_offset(freq)
    return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)
