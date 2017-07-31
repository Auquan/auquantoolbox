import pandas as pd
import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout
from os import listdir
from os.path import isfile, join, basename
from backtester.metrics.metrics import Metrics
from backtester.logger import *

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
def plot(dir, marketFeatures, benchmark, price, startingCapital, excludeFiles):
    if marketFeatures is not None and isfile(marketFeatures):
        logInfo('Generating %s'%marketFeatures)
        df, stats, benchmark_pnl = getDataReady(dir, marketFeatures, benchmark, price, startingCapital, True)
        generateGraph(df, marketFeatures, stats, benchmark_pnl)
    else:
        for fileName in listdir(dir):
            path = dir + '/' + fileName
            if (not isfile(path)) or (path in excludeFiles) or (fileName in excludeFiles):
                print('excluding ', fileName)
                continue
            logInfo('Generating %s'%fileName)
            df, stats, benchmark_pnl = getDataReady(dir, path, benchmark, price, startingCapital, False)
            generateGraph(df, path, fileName + ' ' + stats, benchmark_pnl)

def getDataReady(dir, features, benchmark, price, startingCapital, market=True):
    df = pd.read_csv(features, engine='python')
    df.set_index(df['time'], inplace=True)
    df.index = pd.to_datetime(df.index)
    if market:
        df['Returns(%)'] = 100*(df['pnl']/startingCapital)
        metrics = Metrics(marketFeaturesDf = df)
        metrics.calculateMarketMetrics(benchmark, price, startingCapital, dir)
        benchmark_pnl = metrics.getBenchmarkData(benchmark,price, dir)['returns']
        stats = metrics.getMarketMetricsString()
    else:
        metrics = Metrics(marketFeaturesDf = df)
        metrics.calculateMetrics(price, startingCapital)
        benchmark_pnl = None
        stats = metrics.getMetricsString()
    logInfo(stats)
    return df, stats, benchmark_pnl

def generateGraph(df, fileName, stats, benchmark_pnl):
    layout = dict(
        title= stats,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(count=5,
                         label='5y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )
    plot_data = {
        "data": [],
        "layout": layout
    }
    for col in df.columns[1:]:
        plot_data['data'] += [Scatter(x=df['time'], y=df[col], name = col)]
    if benchmark_pnl is not None:
        plot_data['data'] += [Scatter(x=df['time'], y=100*benchmark_pnl, name = 'Benchmark (%)')]
    plotly.offline.plot(plot_data, filename=fileName+".html")

