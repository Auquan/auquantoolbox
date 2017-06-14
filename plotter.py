import pandas as pd
import numpy as np
import plotly
from plotly import tools
print plotly.__version__  # version >1.9.4 required
from plotly.graph_objs import Scatter, Layout
from os import listdir
from os.path import isfile, join, basename

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
def plot(dir, excludeFiles):
    if isfile(dir):
        fileName = basename(dir)
        generateGraph(dir, fileName)
    else:
        for fileName in listdir(dir):
            path = join(dir, fileName)
            if (not isfile(path)) or (fileName in excludeFiles) :
                continue
            generateGraph(path, fileName)

def generateGraph(path, fileName):
    plot_data = {
        "data": [],
        "layout": Layout(title= fileName + " Plot")
    }
    df = pd.read_csv(path)
    for col in df.columns[1:]:
        plot_data['data'] += [Scatter(x=df['time'], y=df[col], name = col)]
    plotly.offline.plot(plot_data, filename=fileName+".html")
