import pandas as pd
import numpy as np
import plotly
import itertools
from plotly.graph_objs import Scatter, Layout
from plotly.offline import plot
import matplotlib.pyplot as plt
from os import listdir
from sklearn.metrics import confusion_matrix
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

def generateGraph(instrumentList, fileName, statsString, benchmark_pnl, startingCapital=0):
    if isfile(fileName):
        logInfo('Generating %s' % fileName, True)
        updatemenus = list([
        dict(active=-1,
            buttons=list([
                dict(label = 'Total Market',
                    method = 'update',
                    args = [{'title': statsString,
                          'data': generateData(fileName, startingCapital, benchmark_pnl)}])
                ]),
            )
        ])
        layout = dict(
            title=statsString,
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
            ),
            updatemenus=updatemenus
        )

        plot_data = {
            "data": generateData(fileName, startingCapital, benchmark_pnl),
            "layout": layout
        }

        plotly.offline.plot(plot_data, filename=fileName + ".html")

def generateData(fileName, startingCapital, benchmark_pnl):
    df = pd.read_csv(fileName, engine='python',
                     index_col='time', parse_dates=True)
    data = []
    for col in df.columns[1:]:
        data += [Scatter(x=df.index, y=df[col], name=col)]
    if 'pnl' in df.columns and startingCapital>0:
        data += [Scatter(x=df.index, y=100*df['pnl']/float(startingCapital), name='Returns(%)')]
    if benchmark_pnl is not None:
        data += [Scatter(x=df.index,y=100 * benchmark_pnl, name='Benchmark (%)')]
    return data

def generateRegressionModelEvaluationGraph(actual_values, predicted_values):
    trace1 = Scatter(x = actual_values, y = predicted_values, mode = "markers", name = "actual vs predicted",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'))
    p = max(actual_values.max(), predicted_values.max())
    q = min(actual_values.min(), predicted_values.min())
    x1 = np.linspace(p, q)
    y1 = x1
    trace2 = Scatter(x = x1, y = y1, mode = "lines", name = "when actual equals predicted",
                    marker = dict(color = 'rgba(191, 63, 191, 0.8)'))
    data = [trace1, trace2]
    layout = dict(title = 'actual_values vs predicted_values',
              xaxis= dict(title= 'actual_values',ticklen= 5,zeroline= False),
              yaxis= dict(title= 'predicted_values',ticklen= 5,zeroline= False)
             )
    fig = dict(data = data, layout = layout)
    plot(fig)

def generateClassificationModelEvaluationGraph(actual_values, predicted_values, normalize = False):
    cm = confusion_matrix(actual_values, predicted_values)
    cmap = plt.cm.Blues
    length = len(cm)
    title = "confusion matrix without normalization"
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = "confusion matrix with normalization"
    classes = np.unique(actual_values)
    tick_marks = []
    for x in range(length):
        tick_marks.insert(x,np.sum(cm[x]))
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
