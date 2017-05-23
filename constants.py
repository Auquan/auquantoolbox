OPTION_TYPE_CALL = 0
OPTION_TYPE_PUT = 1
OPTION_TYPE_UNDEFINED = -1

BACKTEST = True
PREVIOUS_SAVE_STATE_FILENAME = ''#/home/cjain/trading_scripts/saveState_BANKNIFTY1180189800_2017-05-19.npy'
prev_data = [22831.245,13.118377848,21.6002833831,24974.0178571,24960.3813833,13.5289715346,9.27003813376,0,0,0]
# Constants for running
TIME_INTERVAL_FOR_UPDATES = 30 #  in seconds
ROLL = 0
RF = 0.064
SAMPLE_OPTION_INSTRUMENT_PREFIX = 'BANKNIFTY1180189800'
EXP_DATE = '5/25/2017 15:30:00'
START_TIME = '5/22/2017 09:15:00'

LONG_LIMIT = 12000
SHORT_LIMIT = -12000
OMEGA = 0.25
THRESHOLD = 0.01
MIN_EDGE = 1


#If we don't have yesterday's data
STARTING_FUTURE_VAL = prev_data[0]
STARTING_OPTIONS_DATA = {
'BANKNIFTY118018980021700003' : {'vol' : 0.115},
'BANKNIFTY118018980021800003' : {'vol' : 0.115},
'BANKNIFTY118018980021900003' : {'vol' : 0.115},
'BANKNIFTY118018980022000003' : {'vol' : 0.115},
'BANKNIFTY118018980022100003' : {'vol' : 0.115},
'BANKNIFTY118018980022200003' : {'vol' : 0.115},
'BANKNIFTY118018980022300003' : {'vol' : 0.115},
'BANKNIFTY118018980022400003' : {'vol' : 0.115},
'BANKNIFTY118018980022500003' : {'vol' : 0.115},
'BANKNIFTY118018980022600003' : {'vol' : 0.115},
'BANKNIFTY118018980022700003' : {'vol' : 0.115, 'position' : 0},
'BANKNIFTY118018980022800003' : {'vol' : 0.115, 'position' : 0},
'BANKNIFTY118018980022900003' : {'vol' : 0.115},
'BANKNIFTY118018980023000003' : {'vol' : 0.115},
'BANKNIFTY118018980023100003' : {'vol' : 0.115},
'BANKNIFTY118018980023200003' : {'vol' : 0.115},
'BANKNIFTY118018980023300003' : {'vol' : 0.115},
'BANKNIFTY118018980023400003' : {'vol' : 0.115},
'BANKNIFTY118018980023500003' : {'vol' : 0.115},
'BANKNIFTY118018980023600003' : {'vol' : 0.115},
'BANKNIFTY118018980023700003' : {'vol' : 0.115},
'BANKNIFTY118018980023800003' : {'vol' : 0.115},
'BANKNIFTY118018980023900003' : {'vol' : 0.115},
'BANKNIFTY118018980024000003' : {'vol' : 0.115},
'BANKNIFTY118018980023900004' : {'vol' : 0.115},
'BANKNIFTY118018980023800004' : {'vol' : 0.115},
'BANKNIFTY118018980023700004' : {'vol' : 0.115},
'BANKNIFTY118018980023600004' : {'vol' : 0.115},
'BANKNIFTY118018980023500004' : {'vol' : 0.115},
'BANKNIFTY118018980023400004' : {'vol' : 0.11},
'BANKNIFTY118018980023300004' : {'vol' : 0.115},
'BANKNIFTY118018980023200004' : {'vol' : 0.115},
'BANKNIFTY118018980023100004' : {'vol' : 0.115},
'BANKNIFTY118018980023000004' : {'vol' : 0.115},
'BANKNIFTY118018980022900004' : {'vol' : 0.115},
'BANKNIFTY118018980022800004' : {'vol' : 0.115},
'BANKNIFTY118018980022700004' : {'vol' : 0.115, 'position' : 0},
'BANKNIFTY118018980022600004' : {'vol' : 0.115},
'BANKNIFTY118018980022500004' : {'vol' : 0.115},
'BANKNIFTY118018980022400004' : {'vol' : 0.115},
'BANKNIFTY118018980022300004' : {'vol' : 0.115},
'BANKNIFTY118018980022200004' : {'vol' : 0.115},
'BANKNIFTY118018980022100004' : {'vol' : 0.115},
'BANKNIFTY118018980022000004' : {'vol' : 0.115},
'BANKNIFTY118018980021900004' : {'vol' : 0.115},
'BANKNIFTY118018980021800004' : {'vol' : 0.115},
'BANKNIFTY118018980021700004' : {'vol' : 0.115},
}
START_MARKET_DATA = {'Future': STARTING_FUTURE_VAL,
                    'Vol': prev_data[1]/100.0,
                    'R Vol': prev_data[2]/100.0,
                    'Rolling R Vol': prev_data[2]/100.0,
                    'Close R Vol': prev_data[2]/100.0, 
                    'Mkt_Straddle_low': prev_data[3]/100.0,
                    'Mkt_Straddle_high': prev_data[4]/100.0,
                    }
START_FEATURES_DATA = {'HL AVol': prev_data[5]/100.0,
                    'HL RVol': prev_data[6]/100.0,
                    'HL Rolling RVol': prev_data[6]/100.0,
                    'HL Future': 22755.91427,
                    'Var': 0}
START_POSITON_DATA = {'delta':  prev_data[7],
                    'theta':  prev_data[8],
                    'gamma':  prev_data[9],
                    'total_options': 0}
START_PNL_DATA = {'Pnl': 0, 
                    'Cumulative Pnl' : 0, 
                    'Cash' : 0}
PLACE_ORDER_FILE_NAME = '/spare/local/bose_1/orderData'
Orders_LOG_FILE_PATH = '/home/bose_1/orders/OrdersLogFile'
FUTURE_LOG_FILE_PATH = 'futureLogFile1.txt'
OPTIONS_LOG_FILE_PATH = '/spare/local/bose_1/data.bnifty.options' #set this if just reading from one file during continuous read
CONTINUOS_SAVE_STATE_FILE_PREFIX = "saveState_"
HISTORY_CSV_FILE_PREFIX = "/home/cjain/voldata/"
