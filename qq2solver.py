import os
import os.path
import traceback
import imp
import requests
import json
import time
from backtester.features.feature import Feature
from backtester.trading_system import TradingSystem
from backtester.sample_scripts.fair_value_params import FairValueTradingParams
from backtester.json_utils import getFinalJSON

SECRET_KEY = 'BALLE BALLE'

#API_BASE_URL = 'http://localhost:3002'
API_BASE_URL = 'https://auquan-backend.herokuapp.com'


def getProblemToProcess(subId, probId):
    if not subId or not probId:
        data = {'secretKey': SECRET_KEY}
        url = API_BASE_URL + '/api/getSubmissionForProcessingQQ2'

        r = requests.post(url=url, json=data)
        responseBody = json.loads(r.text)
        if not responseBody.get('submission') or not responseBody.get('submission') != 'None':
            print('no submission to be processed')
            return

        submission = responseBody.get('submission')
        submissionId = submission.get('_id')
        problemId = submission.get('problemId')
        solution = submission.get('solution')
        filename = submissionId + '.py'
        codeFile = open(filename, "w")
        codeFile.write(solution.encode('utf8'))
        codeFile.close()
    else:
        submissionId = subId
        problemId = probId
        filename = submissionId + '.py'
    print('simulating trading system for submission: ' + submissionId)
    result = simulateTradingSystem(filename, str(problemId), str(submissionId))
    resultBody = {'secretKey': SECRET_KEY, 'result': result, 'submissionId': submissionId}

    print('sending result back')
    resultUrl = API_BASE_URL + '/api/updateProcessedSubmission'
    r = requests.post(url=resultUrl, json=resultBody)
    print(r.text)
    print('sent successfully solution for submission: ' + submissionId)


def simulateTradingSystem(tradingSystem, problemId, submissionId):
    if type(tradingSystem) is str:
        tradingSystem = tradingSystem.replace('\\', '/')

    filePathFlag = False
    if str(type(tradingSystem)) =="<type 'classobj'>" or str(type(tradingSystem)) =="<type 'type'>":
        TSobject = tradingSystem()
        solver = TSobject.Problem1Solver()
        tsName = str(tradingSystem)

    elif str(type(tradingSystem)) == "<type 'instance'>" or str(type(tradingSystem)) == "<type 'module'>":
        TSobject = tradingSystem
        solver = TSobject.Problem1Solver()
        tsName = str(tradingSystem)

    elif os.path.isfile(tradingSystem):
        filePathFlag = True
        filePath = str(tradingSystem)
        tsFolder, tsName = os.path.split(filePath)

        try:
            TSobject = imp.load_source('Problem'+problemId+'Solver', filePath)
        except Exception as e:
            print 'Error loading problem solver'
            print str(e)
            print traceback.format_exc()
            return {'error': 'Error loading problem solver' + str(e)}

        try:
            solver = TSobject.Problem1Solver()
        except Exception as e:
            print "Unable to load Problem1Solver. Trying Problem2Solver"
            try:
                solver = TSobject.Problem2Solver()
            except Exception as e1:
                print "Unable to load Problem2Solver as well. Please make sure one of the two is present"
                print str(e)
                print traceback.format_exc()
                return {'error': 'Unable to load Problem1 Or Problem2 solver. Please ensure you solver defintion is correct'}

    else:
        print "Please input your trading system's file path or a callable object."
        return {'error' : 'Error in your submissions. Please contact info@auquan.com'}

    try:
        if len(solver.getSymbolsToTrade()) > 50:
            print "Basket of stocks exceeds maximum value of 50."
            return {'error': 'Symbols to trade exceeds maximum basket value of 50. Please resubmit with a smaller symbol set.'}

        if len(solver.getSymbolsToTrade()) == 0:
            print "Basket of stocks exceeds maximum value of 50 because of empty set."
            return {'error': 'Symbols to trade exceeds maximum basket value of 50. Empty set trades all symbols. Please resubmit with a smaller symbol set.'}

        tsParams = FairValueTradingParams(solver)
        tsParams.setSubmissionId(submissionId)

        for i in ['1', '2', '3']:
            tsParams.setDataSetId('testData' + i)
            tradingSystem = TradingSystem(tsParams)
            tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=False)

        print('Combining result files')
        result = getFinalJSON('testData', submissionId)
        if 'score' in result:
            print(result['score'])
        return result
    except Exception as e:
        print "Error while running backtest"
        message = str(e)
        print message
        print traceback.format_exc()
        if 'updateNum' in message:
            return {'error' : 'Error while running backtest: You are on old version of Auquan Toolbox. Please update your toolbox to version 2.0.0 by running pip install -U auquan_toolbox'}
        return {'error' : 'Error while running backtest: ' + message}


def triggerContinous():
    while True:
        try:
            getProblemToProcess(None, None)
        except Exception as e:
            print "Random error"
            print str(e)
            print traceback.format_exc()
        time.sleep(600)  # Delay for 1 minute (60 seconds)
triggerContinous()
#getProblemToProcess()
