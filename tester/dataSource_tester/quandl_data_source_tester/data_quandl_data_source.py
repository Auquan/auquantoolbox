import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, time, timedelta
from backtester.instrumentUpdates import *

def data_quandl_data_source(c):
    dataSet={}
    parameters={}
    results={}

    if c==0:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False
        parameters["s"]=9
        results["is_number"]=True

    if c==1:
        parameters["lineItem"]="2018/01/"
        results["checkDate"]=False
        parameters["s"]="abc"
        results["is_number"]=False


    if c==2:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False
        parameters["s"]=90.00
        results["is_number"]=True


    if c==3:
        parameters["lineItem"]="2018/01/01"
        results["checkDate"]=False

    if c==5:
        a = {'Open':[191.22497353888585, 189.63061060921606, 198.42955251433312, 199.87444905745895, 206.30175778187137, 207.2683467415234, 208.5837105327601, 205.32520898026894, 206.55087839093568, 206.63059897880115],
             'High':[191.52392125921037, 191.46413430599978, 201.05029135686553, 207.64701504971336, 208.005748726766, 208.51394978684505, 208.76307039590938, 207.07901308566963, 209.04208448157902, 208.36448340030108],
             'Low' :[188.40494119854932, 188.67398049503197, 196.61594750496775, 199.6452620830495, 204.7572070162252, 206.34162505118115, 206.03270353815213, 203.80059184927765, 206.4711578030702, 205.94302310833626],
             'Close':[189.24198345555817, 189.62063582002912, 200.7912109058508, 206.66049145892399, 207.258386899573, 208.3345899236958, 206.38147836973684, 206.5209849143304, 208.14525626784203, 206.799999],
             'Adj Close':[189.24629199999998, 189.624954, 200.795792, 206.665207, 207.26310700000002, 208.33934, 206.386185, 206.52569599999998, 208.149994, 207.529999],
             'Volume':[21029500, 39373000, 67935700, 62404000, 33447400, 25425400, 25587400, 22525500, 23469200, 24611200],
             'Date' : [datetime(2018,7,30),datetime(2018,7,31),datetime(2018,8,1),datetime(2018,8,2),datetime(2018,8,3),datetime(2018,8,6),datetime(2018,8,7),datetime(2018,8,8),datetime(2018,8,9),datetime(2018,8,10)]}
        b = pd.DataFrame(data = a)
        c = b.set_index('Date')
        return c


    return {"dataSet":dataSet,"parameters":parameters,"results":results}
