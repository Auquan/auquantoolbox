import pandas as pd
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


from pandas.tseries.frequencies import to_offset
from functools import partial
import os


def processResult(stats, dir, marketFeatures):
    resultDict = {}
    if marketFeatures is not None and os.path.isfile(marketFeatures):
        df = pd.read_csv(marketFeatures, engine='python',
                         index_col='time', parse_dates=True)
        resultDict['metrics'] = list(stats.keys())
        resultDict['metrics_values'] = list(stats.values())
        resultDict['score'] = stats['Score']

        sampledDf = resampleData(df['pnl'], '1H').last()
        resultDict['dates'] = sampledDf.index.values
        resultDict['total_pnl'] = sampledDf.values
    return resultDict

def resampleData(series, period):
    return series.groupby(partial(round, freq=period))

def round(t, freq):
    freq = to_offset(freq)
    return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)
