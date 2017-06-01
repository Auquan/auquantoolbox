import math
import datetime
from datetime import timedelta
import numpy as np
import datascraper as ds
import option
import future
from constants import *
import useful_fn as utils
import time
import os
import order

def atm_vol(x, y, order):
    delta = 0.5
    if order < 2:
        atmvol = sum(y)/float(len(y))
    elif order < 4:
        p = np.polyfit(x, y, 1)
        atmvol = p[0] * delta + p[1]
    else:
        p = np.polyfit(x, y, 2)
        atmvol = p[0] * delta**2 + p[1] * delta + p[2]
    return atmvol


def shouldUpdateOption(opt, currentFutureVal, currentRoll):
    return (np.abs(opt.k - (currentFutureVal - currentRoll)) < 130)

def getContinuousSaveStateFilename():
    d = utils.convert_time(START_TIME).strftime('%Y%m%d')
    return CONTINUOS_SAVE_STATE_FILE_PREFIX + SAMPLE_OPTION_INSTRUMENT_PREFIX + '_' + d + '.npy'

def getHistoryCsvFilename():
    d = utils.convert_time(START_TIME).date()
    return HISTORY_CSV_FILE_PREFIX + SAMPLE_OPTION_INSTRUMENT_PREFIX + '_' + str(d) + '.csv'

def getRoll(opt_arr, currentFuture):
    s = currentFuture.getFutureVal() - currentFuture.getRoll()
    lowS = int(math.floor(s / 100.0)) * 100
    highS = int(math.ceil(s / 100.0)) * 100
    lowSCallSymbol = str(lowS) + '003'
    lowSPutSymbol =  str(lowS) + '004'
    highSCallSymbol =  str(highS) + '003'
    highSPutSymbol =  str(highS) + '004'
    rf = RF
    t = opt_arr[lowSCallSymbol].t
    s1 = opt_arr[lowSCallSymbol].price - opt_arr[lowSPutSymbol].price + lowS * math.exp(-rf * t)
    s2 = opt_arr[highSCallSymbol].price - opt_arr[highSPutSymbol].price + highS * math.exp(-rf * t)
    updated_s = (s1+s2)/2
    return currentFuture.getFutureVal() - updated_s

def straddle(opt_arr, s):
    lowS = int(math.floor(s / 100.0)) * 100
    highS = int(math.ceil(s / 100.0)) * 100
    lowSCallSymbol = str(lowS) + '003'
    lowSPutSymbol =  str(lowS) + '004'
    highSCallSymbol =  str(highS) + '003'
    highSPutSymbol =  str(highS) + '004'
    std1 = opt_arr[lowSCallSymbol].price + opt_arr[lowSPutSymbol].price
    std2 = opt_arr[highSCallSymbol].price + opt_arr[highSPutSymbol].price
    d1 = opt_arr[lowSCallSymbol].delta + opt_arr[lowSPutSymbol].delta
    d2 = opt_arr[highSCallSymbol].delta + opt_arr[highSPutSymbol].delta
    return std1, std2, d1, d2


# optionsDict - dictionary of options with instrumentId as key, and value as option class
# marketData - dictionary
# featureData - dictionary
# positionData - has delta, theta, gamma, total_options
# returns an array of dictionary of predictions. A prediction looks like this
# {instrumentId: 'OptionName',               name of option, or name of future
#  volume: 5,                                lots you need to buy or sell
#  type: 1}                               1 for BUY or -1 for SELL
def executePredictor(convertedTime, future, optionsDict, marketData, featureData, positionData, threshold):
    # TODO CHADINI:
    futureVal =  future.getFutureVal()
    omega = OMEGA

    curr_vol = marketData['Vol']
    pred = featureData['Prediction']
    edge = pred - curr_vol

    long_lim = LONG_LIMIT
    short_lim = SHORT_LIMIT
    predictions = settle_expiry(convertedTime, optionsDict)
    if len(predictions) == 0:
        predictions = exit_position(convertedTime, futureVal, optionsDict, marketData, featureData, positionData, edge, threshold)
    if len(predictions) == 0:
        predictions = enter_position(convertedTime, futureVal, optionsDict, marketData, featureData, positionData, edge, threshold, long_lim, short_lim)

    return predictions

def get_pred(marketData, featureData, omega):

    Y_hat = featureData['HL AVol'] + 0.1 * (marketData['R Vol'] - featureData['HL AVol']) - 0.25 * (featureData['HL Rolling RVol'] -  marketData['Rolling R Vol'])#+ vcr_iv*(all_data['Future']/all_data['HL Future'] - 1)

    print('Prediction: %.4f'%(float(Y_hat)*100))
    return Y_hat

def isClosingTime(convertedTime):
    convertedTime.time() > utils.convert_time('15:28:00').time():
        return True
    else
        return False

def isExpiry(convertedTime):
    expiry = utils.convert_time(EXP_DATE)
    if  expiry - convertedTime < timedelta(hours=2) :
        return True
    else:
        return False

def calc_retreat(positionData):
    return max(MIN_EDGE, 0.02*np.abs(positionData['total_options'])/400.0)

def at_position_limit(positionData, long_lim, short_lim):
    if (positionData['total_options'] > long_lim) or (positionData['total_options'] < short_lim) :
        return True
    else:
        return False

def get_opt_ref(s):
    CallSymbol =  str(s) + '003'
    PutSymbol = str(s) + '004'
    return CallSymbol, PutSymbol

def settle_expiry(convertedTime, optionsDict):
 #EXPIRY: position goes to zero, no more trading
    predictions = []
    if  isExpiry(convertedTime):
        for instrumentId in optionsDict:
            opt_position = optionsDict[instrumentId].position
            if (opt_position !=0):# if you should trade this option, change this
                prediction = {'instrumentId': instrumentId,
                          'volume': np.abs(opt_position),
                          'type': -np.sign(opt_position)}
                predictions.append(prediction)

    return predictions
def exit_condition(positionData, edge_required, edge, currVol):
    exit_threshold = 0.2*edge_required
    if (positionData['total_options'] < 0):
        if (-edge < exit_threshold) or ((positionData['Last Enter Vol'] - edge_required) > currVol ) or (edge > 0):
            print('Short: Take Profits')
            return True
        elif ((positionData['Last Enter Vol'] + min(3*MIN_EDGE/100, 2*edge_required)) < currVol ):
            print('Short: Hack')
            return True
    elif (positionData['total_options'] > 0):
        if (edge < exit_threshold) or ((positionData['Last Enter Vol'] + edge_required) < currVol ) or (edge < 0):
            print('Long: Take Profits')
            return True
        elif ((positionData['Last Enter Vol'] - min(3*MIN_EDGE/100, 2*edge_required)) > currVol ):
            print('Long: Hack')
            return True
    else:
        return False

def exit_position(convertedTime, futureVal, optionsDict, marketData, featureData, positionData, edge, threshold):
    predictions = []
    retreat = calc_retreat(positionData)
    dte = utils.calculate_t_days(convertedTime, EXP_DATE)
    edge_required = max(MIN_EDGE/100, threshold*(retreat)/np.sqrt(float(dte)))
    if isClosingTime(convertedTime):
        print('Market Close, Getting out')
        for instrumentId in optionsDict:
            opt_position = optionsDict[instrumentId].position
            if (opt_position !=0):# if you should trade this option, change this
                prediction = {'instrumentId': instrumentId,
                          'volume': np.abs(opt_position),
                          'type': -np.sign(opt_position)}
                predictions.append(prediction)

    elif exit_condition(positionData, edge_required, edge, marketData['Vol']):
        print('Getting out','Last Enter Vol: %.2f Actual Edge: %.2f Required: %.2f'%(100*positionData['Last Enter Vol'], 100*edge,100*edge_required*(.3)))
        for instrumentId in optionsDict:
            opt_position = optionsDict[instrumentId].position
            if (opt_position !=0):# if you should trade this option, change this
                prediction = {'instrumentId': instrumentId,
                          'volume': min(80, np.abs(opt_position)),
                          'type': -np.sign(opt_position)}
                predictions.append(prediction)

    return predictions


def enter_position(convertedTime, futureVal, optionsDict, marketData, featureData, positionData, edge, threshold, long_lim, short_lim):
    retreat = calc_retreat(positionData)
    dte = utils.calculate_t_days(convertedTime, EXP_DATE)
    edge_required =  max(MIN_EDGE/100, threshold*(retreat)/np.sqrt(float(dte)))
    if np.abs(positionData['total_options'])>0:
        edge_required = max(0.9*np.abs(positionData['Last Enter Vol'] - marketData['Vol']),edge_required)
    if isExpiry(convertedTime):
        print('Close to Expiry, no trading')
        trade = False
    elif isClosingTime(convertedTime):
        print('Market Closing, no trading')
        trade = False
    elif at_position_limit(positionData, long_lim, short_lim): #or (np.abs(edge) > (3*threshold)):
        print('Position Limit')
        trade = False
    elif np.abs(edge)>(edge_required):
        print('Trading', 'Actual: %.2f Required: %.2f'%(100*edge,100*edge_required))
        trade = True
    else:
        print('Not Enough Edge','Actual: %.2f Required: %.2f'%(100*edge,100*edge_required))
        trade = False

    predictions = []
    if trade:
        atm_call, atm_put = get_opt_ref(int(round(futureVal / 100.0, 0)) * 100)
        atm_options = [atm_call, atm_put]
        for instrumentId in atm_options:
            prediction = {'instrumentId': instrumentId,
                      'volume': 40,
                      'type': np.sign(edge)}
            predictions.append(prediction)
    return predictions

def writeOrder(orderToProcess):
    #orderToProcess = order.Order(instrumentId=instrumentId, tradePrice=tradePrice, vol=volume, time=timeOfUpdate, fees=fees)
    orderFilename = PLACE_ORDER_FILE_NAME
    fd = open(orderFilename, 'a')
    buySell = 'BUY' if orderToProcess.volume > 0 else 'SELL'
    data = ['PLACE_MKT', SAMPLE_OPTION_INSTRUMENT_PREFIX + str(orderToProcess.instrumentId), np.abs(orderToProcess.volume), buySell ]
    fd.write(' '.join(map(str, data)) + '\n')
    fd.close()

class UnderlyingProcessor:
    def __init__(self, futureVal, optionsData, startMarketData, startFeaturesData, startPositionData, startPnlData, startTime):
        self.histFutureInstruments = []  # for storing history of future instruments
        self.histOptionInstruments = {}  # for storing history of option instruments
        # secondsInterval = pd.date_range(start=START_DATE, end=END_DATE, freq='1S')
        # self.marketData = pd.DataFrame(index=secondsInterval, columns=['Future', 'Vol', 'Mkt_Straddle', 'Theo_Straddle'])

        self.marketData = [startMarketData]
        self.features = [startFeaturesData]
        self.lastTimeSaved = utils.convert_time(startTime)
        self.currentFuture = future.Future(futureVal, ROLL, startTime)
        self.currentOptions = {}
        self.positionData = [startPositionData]
        self.pnlData = [startPnlData] # TODOKANAV: Put in constants
        for instrumentId in optionsData:
            optionData = optionsData[instrumentId]
            opt = option.Option(underlyingPrice=futureVal - ROLL,
                                instrumentId=instrumentId,
                                exp_date=EXP_DATE,
                                instrumentPrefix=SAMPLE_OPTION_INSTRUMENT_PREFIX,
                                eval_date=startTime,
                                vol=optionData['vol'],
                                rf=RF,
                                position=optionData['position'] if 'position' in optionData else 0)
            self.currentOptions[instrumentId] = opt
        self.totalTimeUpdating = 0
        self.totalIter = 0
        self.printCurrentState()

    def serializeCurrentState(self):
        stateToSave = {}
        stateToSave['futureVal'] = self.currentFuture.getFutureVal()
        stateToSave['marketData'] = self.marketData[-1]
        stateToSave['featureData'] = self.features[-1]
        stateToSave['time'] = self.lastTimeSaved
        optionDataToSave = {}
        for instrumentId in self.currentOptions:
            optionDataToSave[instrumentId] = {
                'vol': self.currentOptions[instrumentId].vol,
                'position': self.currentOptions[instrumentId].position}
        stateToSave['options'] = optionDataToSave
        stateToSave['positionData'] = self.positionData[-1]
        stateToSave['pnlData'] = self.pnlData[-1]
        return stateToSave

    def printCurrentState(self, isVerbose=False):
        currentState = self.serializeCurrentState()
        timeToPrint = currentState['time'].strftime('%H:%M:%S')
        futureValToPrint = '%.2f' % currentState['futureVal']
        volToPrint = '%.2f' % (currentState['marketData']['Vol'] * 100)
        rvolToPrint = '%.2f' % (currentState['marketData']['R Vol'] * 100)
        mktLowToPrint = '%.2f' % (currentState['marketData'][
                                  'Mkt_Straddle_low'] * 100)
        mktHighToPrint = '%.2f' % (currentState['marketData'][
                                   'Mkt_Straddle_high'] * 100)
        hlavolToPrint = '%.2f' % (currentState['featureData']['HL AVol'] * 100)
        hlrvolToPrint = '%.2f' % (currentState['featureData']['HL Rolling RVol'] * 100)
        positionDelta = '%.2f' % currentState['positionData']['delta']
        positionGamma = '%.2f' % currentState['positionData']['gamma']
        positionTheta = '%.2f' % currentState['positionData']['theta']
        pnl = '%.2f' % currentState['pnlData']['Pnl']
        cumulative_pnl = '%.2f' % currentState['pnlData']['Cumulative Pnl']
        # print '\n\n\n\n\n'
        print '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (timeToPrint, futureValToPrint, volToPrint, rvolToPrint, mktLowToPrint, mktHighToPrint, hlavolToPrint, hlrvolToPrint, positionDelta, positionGamma, positionTheta, pnl, cumulative_pnl)
        if not isVerbose:
            return
        print 'Time: ' + str(currentState['time'])
        print 'Future Value: ' + str(currentState['futureVal'])
        print 'Average Time for update: ' + str(0 if self.totalIter == 0 else self.totalTimeUpdating / self.totalIter)
        print '----------Market Data----------'
        print currentState['marketData']
        print '----------Feature Data---------'
        print currentState['featureData']
        print '---------Options---------------'
        print currentState['options']

    def saveCurrentState(self):
        serializedState = self.serializeCurrentState()
        # save last
        np.save(getContinuousSaveStateFilename(), serializedState)
        # save in history
        # TODO: Save other values in csv also
        historyCsvFilename = getHistoryCsvFilename()
        stateDataArray = [serializedState['time'].strftime('%H:%M:%S')]
        stateDataArray.append(serializedState['futureVal'])
        stateDataArray.append(serializedState['marketData']['Vol'] * 100)
        stateDataArray.append(serializedState['marketData']['R Vol'] * 100)
        stateDataArray.append(serializedState['marketData']['Rolling R Vol'] * 100)
        stateDataArray.append(serializedState['marketData'][
                              'Mkt_Straddle_low'] * 100)
        stateDataArray.append(serializedState['marketData'][
                              'Mkt_Straddle_high'] * 100)
        stateDataArray.append(serializedState['featureData']['HL AVol'] * 100)
        stateDataArray.append(serializedState['featureData']['HL RVol'] * 100)
        stateDataArray.append(serializedState['featureData']['Prediction'] * 100)
        stateDataArray.append(serializedState['positionData']['delta'])
        stateDataArray.append(serializedState['positionData']['gamma'])
        stateDataArray.append(serializedState['positionData']['theta'])
        stateDataArray.append(serializedState['pnlData']['Cumulative Pnl'])
        csvRow = ','.join(map(str, stateDataArray)) + '\n'
        fd = open(historyCsvFilename, 'a')
        fd.write(csvRow)
        fd.close()

    # updates features at regular intervals only
    def updateFeatures(self, timeOfUpdate):
        convertedTime = utils.convert_time(timeOfUpdate)
        if (convertedTime < self.lastTimeSaved + timedelta(0, TIME_INTERVAL_FOR_UPDATES)):
            return

        lastTimeSaved = self.lastTimeSaved
        self.lastTimeSaved = convertedTime
        # tracking perf
        start = time.time()

        currentFutureVal = self.currentFuture.getFutureVal()
        if currentFutureVal == 0:
            print('Future not trading')
        else:
            self.updateRoll()
            self.updateOptionVol()
            marketDataDf, featureDf = getFeaturesDf(
                convertedTime, lastTimeSaved, self.currentFuture, self.currentOptions, self.marketData[-1], self.features[-1])

            if marketDataDf is not None:
                self.marketData.append(marketDataDf)
            if featureDf is not None:
                self.features.append(featureDf)

            # executing predictor
            predictions = executePredictor(convertedTime, self.currentFuture, self.currentOptions, self.marketData[-1], self.features[-1], self.positionData[-1], THRESHOLD)

            #executing trades based on predictions
            self.updatePositionPnlWithPredictions(predictions, timeOfUpdate)

            self.lastTimeSaved = convertedTime
            # Savingstate
            self.saveCurrentState()

            end = time.time()
            diffms = (end - start) * 1000
            self.totalTimeUpdating = self.totalTimeUpdating + diffms
            self.totalIter = self.totalIter + 1
            self.printCurrentState()

    def updateWithNewFutureInstrument(self, futureInstrument):
        # self.histFutureInstruments.append(instrument)  # just for storing
        self.updateFeatures(futureInstrument.time)
        self.currentFuture.updateWithNewInstrument(futureInstrument)
        #self.updateFeatures(futureInstrument.time)

    def updateWithNewOptionInstrument(self, optionInstrument):
        # self.addNewOption(optionInstrument)  # just for storing
        self.updateFeatures(optionInstrument.time)
        if optionInstrument.instrumentId in self.currentOptions :
            changedOption = self.currentOptions[optionInstrument.instrumentId]
        else:
            changedOption = option.Option(underlyingPrice = self.currentFuture.getFutureVal() - self.currentFuture.getRoll(),
                                instrumentId = optionInstrument.instrumentId,
                                exp_date = EXP_DATE,
                                instrumentPrefix = SAMPLE_OPTION_INSTRUMENT_PREFIX,
                                eval_date = optionInstrument.time,
                                vol = 0.16,
                                rf = RF,
                                position = 0)
            self.currentOptions[optionInstrument.instrumentId] = changedOption


        changedOption.updateWithInstrument(optionInstrument, self.currentFuture)
        #self.updateFeatures(optionInstrument.time)

    def updateWithNewOrder(self, order):
        if order.isFuture():
            self.currentFuture.updateWithOrder(order)
        else:
            changedOption = self.currentOptions[order.instrumentId]
            changedOption.updateWithOrder(order)
        self.updateFeatures(order.time)

    def updatePositionPnlWithPredictions(self, predictions, timeOfUpdate):
        cash_used = 0
        if len(predictions)>0 and os.path.isfile(PLACE_ORDER_FILE_NAME):
            os.remove(PLACE_ORDER_FILE_NAME)

        for prediction in predictions:
            instrumentId = prediction['instrumentId']
            volume = prediction['volume']
            if prediction['type'] != 1:
                volume = -volume
            tradePrice = 0
            optionToOrder = self.currentOptions[instrumentId]

            if optionToOrder:
                tradePrice = optionToOrder.price
            elif instrumentId == self.currentFuture:
                # TODO handle this
                tradePrice = self.currentFuture.getFutureVal()
            else:
                continue

            fees = tradePrice * 0.001
            cash_used += float(volume)*float(tradePrice)  + float(fees)
            print(instrumentId, '%.2f'%tradePrice, volume)
            orderToProcess = order.Order(instrumentId=instrumentId, tradePrice=tradePrice, vol=volume, time=timeOfUpdate, fees=fees)
            if BACKTEST:
                self.updateWithNewOrder(orderToProcess)
            else:
                writeOrder(orderToProcess)

        # Calculating updates position data
        positionsDf, pnlDf = getPosition_PnlDf(self.currentFuture, self.currentOptions, self.positionData[-1], self.marketData[-1], self.pnlData[-1], cash_used)
        if positionsDf is not None:
            self.positionData.append(positionsDf)
        self.pnlData.append(pnlDf)

    def updateRoll(self):
        roll = getRoll(self.currentOptions, self.currentFuture)
        self.currentFuture.updateRoll(roll)

    def updateOptionVol(self):
        for instrumentId in self.currentOptions:
            opt = self.currentOptions[instrumentId]
            if shouldUpdateOption(opt, self.currentFuture.getFutureVal(), self.currentFuture.getRoll()):
                opt.s = self.currentFuture.getFutureVal() - self.currentFuture.getRoll()
                opt.get_impl_vol()
    '''
    ------------------------------------------------------
    ----------- For storing stuff ------------------------
    ------------------------------------------------------
    '''
    def getCurrentFuture(self):
        return self.histFutureInstruments[-1]

    # returns dictionary of instrumentId -> Option class object
    def getAllCurrentOptions(self):
        toRtn = {}
        for instrumentId in self.histOptionInstruments:
            toRtn[instrumentId] = self.histOptionInstruments[instrumentId][-1]
        return toRtn

    # returns Option class object
    def getCurrentOption(self, instrumentId):
        self.ensureInstrumentId(instrumentId)
        # TODO: what happens if array is empty
        return self.histOptionInstruments[instrumentId][-1]

    def ensureInstrumentId(self, instrumentId):
        if instrumentId not in self.histOptionInstruments:
            self.histOptionInstruments[instrumentId] = []

    def addNewOption(self, opt):
        self.ensureInstrumentId(opt.instrumentId)
        self.histOptionInstruments[opt.instrumentId].append(opt)

    '''
    ------------------------------------------------------
    ----------- Process new data -------------------------
    ------------------------------------------------------
    '''
    def processData(self, instrumentsToProcess):
        for instrument in instrumentsToProcess:
            if utils.convert_time(instrument.time).time() >utils.convert_time('15:30:00').time():
                continue
            if instrument.isFuture():
                self.updateWithNewFutureInstrument(instrument)
            else:
                self.updateWithNewOptionInstrument(instrument)

    def processOrders(self, ordersToProcess):
        for order in ordersToProcess:
            self.updateWithNewOrder(order)


def getPosition_PnlDf(future, opt_dict, positionData, marketData, previousPnl, cash_used):
    futureVal =  future.getFutureVal()
    options_arr = []
    for instrumentId in opt_dict:
        if opt_dict[instrumentId].position != 0:
            options_arr.append(opt_dict[instrumentId])

    temp_positiondf = {}
    temp_pnldf = {}
    temp_positiondf['delta'] = 0
    temp_positiondf['gamma'] = 0
    temp_positiondf['theta'] = 0
    temp_positiondf['total_options'] = 0
    temp_pnldf['Cash'] = previousPnl['Cash'] - cash_used
    instrumentsValue = 0

    if future.position != 0:
        temp_positiondf['delta'] += float(future.position) * 1
        instrumentsValue += float(future.position) * float(futureVal)

    for opt in options_arr:
        price, delta, theta, gamma = opt.get_all()
        temp_positiondf['delta'] += float(opt.position) * delta
        temp_positiondf['gamma'] += float(opt.position) * gamma
        temp_positiondf['theta'] += float(opt.position) * theta
        temp_positiondf['total_options'] += float(opt.position)
        instrumentsValue += float(opt.position) * float(price)

    if np.abs(temp_positiondf['total_options']) > np.abs(positionData['total_options']):
        temp_positiondf['Last Enter Vol'] = marketData['Vol']
        temp_positiondf['Last Exit Vol'] = positionData['Last Exit Vol']
    elif np.abs(temp_positiondf['total_options']) < np.abs(positionData['total_options']):
        temp_positiondf['Last Exit Vol'] = marketData['Vol']
        temp_positiondf['Last Enter Vol'] = positionData['Last Enter Vol']
    else:
        temp_positiondf['Last Enter Vol'] = positionData['Last Enter Vol']
        temp_positiondf['Last Exit Vol'] = positionData['Last Exit Vol']

    #print(cash_used, instrumentsValue, temp_pnldf['Cash'])
    temp_pnldf['Cumulative Pnl'] = instrumentsValue + temp_pnldf['Cash']
    temp_pnldf['Pnl'] = temp_pnldf['Cumulative Pnl'] - previousPnl['Cumulative Pnl'] #+ temp_pnldf['Pnl']
    return temp_positiondf, temp_pnldf


def getFeaturesDf(convertedTime, lastTimeSaved, future, opt_dict, lastMarketDataDf, lastFeaturesDf):
    currentFutureVal = future.getFutureVal()
    roll = future.getRoll()
    if currentFutureVal == 0:
        print('Future not trading')
        return None, None
    else:
        temp_df = {}
        temp_f = {}

        temp_df['Future'] = currentFutureVal
        temp_df['Roll'] = roll
        delta_arr = []
        vol_arr = []
        var = 0
        try:
            # Loop over all options and get implied vol for each option
            for instrumentId in opt_dict:
                opt = opt_dict[instrumentId]
                if not shouldUpdateOption(opt, currentFutureVal, roll):
                    continue
                opt.get_price_delta()
                price, delta = opt.calc_price, opt.delta
                if abs(delta) < 0.7 and abs(delta) > 0.3 :
                    if (delta < 0):
                        delta = 1 + delta
                    delta_arr.append(delta)
                    # TODO: ivol?
                    vol_arr.append(opt.vol)
            print(roll, vol_arr, delta_arr)
            # Calculate ATM Vol
            if len(delta_arr) > 0:
                temp_df['Vol'] = atm_vol(delta_arr, vol_arr, len(delta_arr)-1)
                delta_arr.append(0.5)
                vol_arr.append(temp_df['Vol'])
            else:
                temp_df['Vol'] = lastMarketDataDf['Vol']

            temp_df['Mkt_Straddle_low'], temp_df[
                    'Mkt_Straddle_high'], delta_low, delta_high = straddle(opt_dict, currentFutureVal - roll)
            # Calculate Intraday and Rolling Realized Vol
            #print('>>>>Checking R Vol Calcs', 'Curr Time', convertedTime.date(), 'Last Time', lastTimeSaved.date())
            #print('>>>>','Last Future %0.2f Curr Future %0.2f'%( lastFeaturesDf['Last Move Future'],fut))
            if convertedTime.date() != lastTimeSaved.date() :
                lastVar = 0
                temp_df['Close R Vol'] = lastMarketDataDf['R Vol']
                lastFuture = lastFeaturesDf['Last Move Future'] - FUTURE_ROLL_FROM_EXPIRY
            else:
                lastVar = lastFeaturesDf['Var']
                temp_df['Close R Vol'] = lastMarketDataDf['Close R Vol']
                lastFuture = lastFeaturesDf['Last Move Future']

            if np.abs(currentFutureVal - lastFuture) > VAR_THRESHOLD:
                var = utils.calc_var_RT(lastVar, currentFutureVal, lastFuture)
                temp_f['Last Move Future'] = currentFutureVal
                #print('>>>>','Future moved, updating var: %0.6f'%var)
            else:
                var = lastVar
                temp_f['Last Move Future'] = lastFuture
                #print('>>>>','Future no move, not updating var: %0.6f'%var)

            temp_f['Var'] = var
            idx = convertedTime.ceil('min').strftime('%H:%M')
            day_winddown = 1 - utils.calculate_t_days(
                            convertedTime, convertedTime.replace(hour=15, minute=30, second=0))
            temp_f['varDict'] = lastFeaturesDf['varDict']
            lastIdx = temp_f['varDict']['lastIdx']
            #print('>>>>','Last Index: %s Curr Index %s Winddown %0.2f'%(lastIdx, idx, day_winddown))

            if  lastIdx != idx :
                temp_f['varDict'][lastIdx] = lastFeaturesDf['Var']
                #print('>>>>','Updating value of ', lastIdx)

            try:
                temp_df['Rolling R Vol'] =  np.sqrt(252 * (var - temp_f['varDict'][idx])+ lastMarketDataDf['Close R Vol']**2 )
                #print('>>>>','Curr var %.6f Idx Var %s Rolling RV %.4f'%(var, temp_f['varDict'][idx], temp_df['Rolling R Vol']))
            except KeyError:
                temp_df['Rolling R Vol'] =  np.sqrt((252 * (var)+ lastMarketDataDf['Close R Vol']**2 )/(1+day_winddown))
                #print('>>>>','We dont have prev varDict Curr var %.6f Rolling RV %.4f '%(var, temp_df['Rolling R Vol']))
            if day_winddown > 0:
                temp_df['R Vol'] = np.sqrt(252 * var /day_winddown)
            else:
                temp_df['R Vol'] = 0
            #print('>>>>','Curr var %.6f RV %.4f '%(var, temp_df['R Vol']))
            temp_f['varDict']['lastIdx'] = idx

            # Calculate Features
            hl_iv = 22500/ float(TIME_INTERVAL_FOR_UPDATES)
            hl_rv = hl_iv * 3
            if utils.convert_time(EXP_DATE)  - convertedTime < timedelta(minutes=180):
                temp_f['HL AVol'] = lastFeaturesDf['HL AVol']
            else:
                temp_f['HL AVol'] = utils.ema_RT(
                    lastFeaturesDf['HL AVol'], temp_df['Vol'], hl_iv)
            temp_f['HL RVol'] = utils.ema_RT(
                lastFeaturesDf['HL RVol'], temp_df['R Vol'], hl_rv)
            temp_f['HL Rolling RVol'] = utils.ema_RT(
                lastFeaturesDf['HL Rolling RVol'], temp_df['Rolling R Vol'], hl_rv)
            temp_f['HL Future'] = utils.ema_RT(
                lastFeaturesDf['HL Future'], temp_df['Future'], hl_iv)
            omega = OMEGA
            temp_f['Prediction'] = get_pred(temp_df, temp_f, omega)

            print('RV: Close %.2f Rolling %.2f ID %.2f HL ID: %.2f HL Roll %.2f'%(
                100*temp_df['Close R Vol'], 100*temp_df['Rolling R Vol'], 100*temp_df['R Vol'], 100*temp_f['HL RVol'], 100*temp_f['HL Rolling RVol']))
	    # append data
            return temp_df, temp_f

        except:
            raise
            return lastMarketDataDf, lastFeaturesDf


def followFiles(files):
    for f in files:
        f.seek(0, 2)
    unfinishedLines = [''] * len(files)
    while True:
        readLines = list(map(lambda x: x.readline(), files))
        readOneLine = False
        i = 0
        for readLine in readLines:
            if readLine:
                readOneLine = True
                unfinishedLines[i] = unfinishedLines[i] + readLine
                if unfinishedLines[i].endswith('\n'):
                    yield(i, unfinishedLines[i])
                    unfinishedLines[i] = ''
            i = i + 1

        if not readOneLine:
            time.sleep(0.1)


    logFile.seek(0, 2)
    while True:
        logLine = logFile.readline()
        if not logLine:
            time.sleep(0.1)
            continue
        yield(logLine)


def createHistoryCsvFileIfNeeded():
    historyCsvFilename = getHistoryCsvFilename()
    if os.path.isfile(historyCsvFilename):
        return
    fd = open(historyCsvFilename, 'a')
    headers = ['Time', 'Future', 'Vol', 'ID R Vol', 'Rolling R Vol',
               'Straddle_low', 'Straddle_high', 'HL AVol', 'HL RVol', 'Prediction', 'position_delta', 'position_gamma', 'position_theta', 'Cumulative Pnl']
    fd.write(','.join(map(str, headers)) + '\n')
    fd.close()


# Follows log files continuously and runs the strategy.
# Saves state continuously. if State has been saved runs from the last saved state
# else runs from constants.py
def startStrategyContinuous():
    createHistoryCsvFileIfNeeded()
    up = None
    if os.path.isfile(getContinuousSaveStateFilename()):
        print 'Reading from saved state'
        stateSaved = np.load(getContinuousSaveStateFilename()).item()
        up = UnderlyingProcessor(stateSaved['futureVal'], stateSaved['options'], stateSaved[
            'marketData'], stateSaved['featureData'], stateSaved['positionData'], stateSaved['pnlData'], stateSaved['time'])
    elif os.path.isfile(PREVIOUS_SAVE_STATE_FILENAME):
        print 'Reading from previous saved state'
        stateSaved = np.load(PREVIOUS_SAVE_STATE_FILENAME).item()
        up = UnderlyingProcessor(stateSaved['futureVal'], stateSaved['options'], stateSaved[
           'marketData'], stateSaved['featureData'], stateSaved['positionData'], stateSaved['pnlData'], stateSaved['time'])
    else:
        print 'Reading from constants'
        up = UnderlyingProcessor(STARTING_FUTURE_VAL, STARTING_OPTIONS_DATA,
                                 START_MARKET_DATA, START_FEATURES_DATA, START_POSITON_DATA, START_PNL_DATA, START_TIME)

    instrumentsDataparser = ds.Dataparser()
    positionsDataparser = ds.OrdersParser()
    logFile = open(OPTIONS_LOG_FILE_PATH, "r")
    ordersFile = open(Orders_LOG_FILE_PATH, "r")
    lines = followFiles([logFile, ordersFile])
    for line in lines:
        (t, lineContent) = line
        if len(lineContent) == 0:
            continue
        if t == 0:
            optionInstrumentsToProcess = instrumentsDataparser.processLines([
                lineContent])
            up.processData(optionInstrumentsToProcess)
        elif t == 1:
            ordersToProcess = positionsDataparser.processLines([lineContent])
            up.processOrders(ordersToProcess)


def startStrategyHistory(historyFilePath):
    createHistoryCsvFileIfNeeded()
    up = None
    if os.path.isfile(PREVIOUS_SAVE_STATE_FILENAME):
        print 'Reading from previous saved state'
        stateSaved = np.load(PREVIOUS_SAVE_STATE_FILENAME).item()
        up = UnderlyingProcessor(stateSaved['futureVal'], stateSaved['options'], stateSaved[
            'marketData'], stateSaved['featureData'], stateSaved['positionData'], stateSaved['pnlData'], stateSaved['time'])
    else:
        print 'Reading from constants'
        up = UnderlyingProcessor(STARTING_FUTURE_VAL, STARTING_OPTIONS_DATA,
                                 START_MARKET_DATA, START_FEATURES_DATA, START_POSITON_DATA, START_PNL_DATA, START_TIME)
    dataParser = ds.Dataparser()
    with open(historyFilePath) as f:
        for line in f:
            instrumentsToProcess = dataParser.processLines([line])
            up.processData(instrumentsToProcess)

if BACKTEST:
    print('Running Backtest')
    startStrategyHistory(HISTORICAL_DATA_FILE)
else:
    print('Running Live')
    startStrategyContinuous()

