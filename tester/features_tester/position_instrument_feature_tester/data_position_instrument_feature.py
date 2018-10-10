import pandas as pd
import numpy as np
def getDataSet(c):
    dataSet={}
    parameters={}
    results={}
#### empty dataSets, returns empty dict
    if(c==0):
        dataSet["dict"]={}
        results["positionInstrument_Instrument1"]={}
        results["positionInstrument_Instrument2"]={}
#### sample dataset
    if(c==1):
        dataSet["dict"]={'a':1,'b':2}
        results["positionInstrument_Instrument1"]={'a':10, 'b': 20}
        results["positionInstrument_Instrument2"]={'a':20, 'b': 10}
    return {"dataSet":dataSet, "parameters":parameters, "results":results}
