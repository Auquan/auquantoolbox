import math
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import greeks
import datascraper as ds
import os
import future
import instrument
import option


def atm_vol(x, y, order):
    delta = 0.5
    if order == 2:
        p = np.polyfit(x, y, 1)
        atmvol = p[0] * delta + p[1]
    else:
        p = np.polyfit(x, y, 2)
        atmvol = p[0] * delta**2 + p[1] * delta + p[2]
    return atmvol

def get_index_val(fut, roll):
    # rf = opt_arr[0].rf
    # t = opt_arr[0].t
    # s1 = opt_arr[1].price - opt_arr[0].price + opt_arr[0].k * math.exp(-rf * t)
    # s2 = opt_arr[3].price - opt_arr[2].price + opt_arr[2].k * math.exp(-rf * t)
    return fut - roll


def straddle(opt_arr, s):
    lowS = int(math.floor(s / 100.0)) * 100
    highS = int(math.ceil(s / 100.0 )) * 100
    lowSCallSymbol = SAMPLE_OPTION_INSTRUMENT_PREFIX + str(lowS) + '003'
    lowSPutSymbol = SAMPLE_OPTION_INSTRUMENT_PREFIX + str(lowS) + '004'
    highSCallSymbol = SAMPLE_OPTION_INSTRUMENT_PREFIX + str(highS) + '003'
    highSPutSymbol = SAMPLE_OPTION_INSTRUMENT_PREFIX + str(highS) + '004'
    std1 = opt_arr[lowSCallSymbol].price + opt_arr[lowSPutSymbol].price
    std2 = opt_arr[highSCallSymbol].price + opt_arr[highSPutSymbol].price
    d1 = opt_arr[lowSCallSymbol].delta + opt_arr[lowSPutSymbol].delta
    d2 = opt_arr[highSCallSymbol].delta + opt_arr[highSPutSymbol].delta
    return std1,std2,d1,d2

FILE_PATH = 'C:/Users/Chandini/Nifty_Project'
SAMPLE_OPTION_INSTRUMENT_PREFIX = 'BANKNIFTY1152973800'
exp_date ='5/4/2017 15:30:00'
rf = 0.065 
roll = 45

class UnderlyingProcessor:
    def __init__(self, trade_date):
        self.trade_date = trade_date
        self.futures = []
        self.histOptions = {}

    # returns Future class object
    def getCurrentFuture(self):
        return self.futures[-1]

    # returns dictionary of instrumentId -> Option class object
    def getAllCurrentOptions(self):
        toRtn = {}
        for instrumentId in self.histOptions:
            toRtn[instrumentId] = self.histOptions[instrumentId][-1]
        return toRtn

    # returns Option class object
    def getCurrentOption(self, instrumentId):
        self.ensureInstrumentId(instrumentId)
        return self.histOptions[instrumentId][-1] # TODO: what happens if array is empty

    def ensureInstrumentId(self, instrumentId):
        if instrumentId not in self.histOptions:
            self.histOptions[instrumentId] = []

    def addNewOption(self,opt):
        self.ensureInstrumentId(opt.instrumentId)
        self.histOptions[opt.instrumentId].append(opt)

    def processData(self):
        filename = '%s/%s/data' % (FILE_PATH, self.trade_date)
        instrumentsToProcess = ds.loadData(filename)  # TODO
        data = pd.DataFrame(index=[], columns=['Future', 'Vol',
                                               'Mkt_Straddle', 'Theo_Straddle'])
        for instrument in instrumentsToProcess:
            if instrument.isFuture():
                self.futures.append(currentFuture)
                # todo: update price of options
            else:
                s = get_index_val(self.getCurrentFuture(), roll)
                opt = option.Option(futurePrice=self.getCurrentFuture().futureVal,
                                    optionInstrument=instrument,
                                    exp_date=exp_date,
                                    instrumentPrefix=SAMPLE_OPTION_INSTRUMENT_PREFIX,
                                    rf=rf)
                #Update s and vol
                opt.s = s
                opt.get_impl_vol()
                self.addNewOption(opt)
                # todo: update future value store it in data



var = 0
data = pd.DataFrame(index=[], columns=[
                    'Future', 'Vol', 'Mkt_Straddle_low','Mkt_Straddle_high'])
features = pd.DataFrame(index=[], columns=[
                    'HL AVol', 'HL RVol', 'HL Future', 'Pred'])
up = UnderlyingProcessor(trade_date)
runLoop = True
while runLoop:
    eval_date = datetime.now()
    
    #stop when it is 3:30 pm
    if eval_date.time() > time(15,30):
        runLoop = False
        continue
    
    up.processData()
    fut = up.getCurrentFuture()
    opt_dict = up.getAllCurrentOptions()
    if fut == 0:
        print('Future not trading')
        continue
    else:
        temp_df = pd.DataFrame(index=[eval_date], columns=[
                               'Future', 'Vol', 'Mkt_Straddle_low','Mkt_Straddle_high'])
        temp_df['Future'] = fut
        delta_arr = []
        vol_arr = []
        try:
            
            #Loop over all options and get implied vol for each option
            for j in opt_dict.keys():
                opt = opt_dict[j]
                opt.get_price_delta()
                price, delta =  opt.calc_price, opt.delta
                if abs(delta) <0.75:
                    if (delta < 0):
                        delta = 1 + delta
                    delta_arr.append(delta)
                    vol_arr.append(ivol)
            
            #Calculate ATM Vol
            if len(delta_arr)>0:
                temp_df['Vol'] = atm_vol(delta_arr, vol_arr, 2)
                temp_df['Mkt_Straddle_low'] ,temp_df['Mkt_Straddle_high'], delta_low, delta_high = straddle(opt_arr, s)
                delta_arr.append(0.5)
                vol_arr.append(temp_df['Vol'])
            else:
                temp_df['Vol'] = data['Vol'].iloc[-1]

            #Calculate Realized Vol
            var = calc_var_RT(var,fut, data['Future'].iloc[-1] )
            temp_df['R Vol'] = np.sqrt(252*var/(1-calculate_t(eval_date,eval_date.date()+timedelta(15,30,00))))

            #Calculate Features
            temp_f['HL AVol'] = ema_RT(features['HL AVol'].iloc[-1], temp_df['Vol'], hl_iv)
            temp_f['HL RVol'] = ema_RT(features['HL RVol'].iloc[-1], temp_df['R Vol'], hl_rv)
            temp_f['HL Future'] = ema_RT(features['HL Future'].iloc[-1], temp_df['Future'], hl_iv)

            #Combine Features into prediction
            temp_f['Pred'] = temp_f['HL AVol'] + temp_f['HL RVol']  + temp_df['Future']/temp_f['HL Future'] - 1

            #Print
            print(pd.DataFrame(zip(delta_arr, vol_arr),columns=['Delta','IVol']))
            print('Low Straddle',delta_low,temp_df['Mkt_Straddle_low'] )
            print('High Straddle', delta_high,temp_df['Mkt_Straddle_high'])
            print(temp_df, temp_f)

            #append data
            data = data.append(temp_df)
            features = features.append(temp_f)
        
        except:
            continue
