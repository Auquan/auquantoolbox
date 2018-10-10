def data_base_execution_system():
    parameters={}
    results={}
    parameters["time"]="01/01/2010"
    parameters["instrumentId"]=dict={'1':1,'2':2}
    parameters["volume"]=10
    parameters["executionType"]="abc"
    parameters["capital"]=10
    results["getExecutions"]=[]
    results["getExecutionsAtClose"]=[]
    return {"parameters":parameters,"results":results}
