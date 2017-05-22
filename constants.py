OPTION_TYPE_CALL = 0
OPTION_TYPE_PUT = 1
OPTION_TYPE_UNDEFINED = -1


# Constants for running
TIME_INTERVAL_FOR_UPDATES = 5  # in seconds
ROLL = 45
RF = 0.065
STARTING_FUTURE_VAL = 22400.0
STARTING_OPTIONS_DATA = {
    'BANKNIFTY117837540022500003': {'vol': 0.2},
    'BANKNIFTY117837540022600003': {'vol': 0.3},
    'BANKNIFTY117837540022700003': {'vol': 0.3},
    'BANKNIFTY117837540022800003': {'vol': 0.3},
    'BANKNIFTY117837540022900003': {'vol': 0.3},
    'BANKNIFTY117837540022400003': {'vol': 0.3},
    'BANKNIFTY117837540022300003': {'vol': 0.3},
    'BANKNIFTY117837540022200003': {'vol': 0.3},
    'BANKNIFTY117837540022100003': {'vol': 0.3},
    'BANKNIFTY117837540022000003': {'vol': 0.3},
    'BANKNIFTY117837540022200004': {'vol': 0.4},
    'BANKNIFTY117837540022300004': {'vol': 0.4},
    'BANKNIFTY117837540022400004': {'vol': 0.4},
    'BANKNIFTY117837540022500004': {'vol': 0.4},
}
START_MARKET_DATA = {'Future': STARTING_FUTURE_VAL,
                     'R Vol': 0,
                     'Vol': 0,
                     'Mkt_Straddle_low': 0,
                     'Mkt_Straddle_high': 0,
                     'Theo_Straddle': 0}
START_FEATURES_DATA = {'HL AVol': .39,
                       'HL RVol': 0,
                       'HL Future': 0,
                       'Pred': 0,
                       'Var': 0}
START_POSITON_DATA = {'delta': 0,
                      'theta': 0,
                      'gamma': 0,
                      'total_options': 0}
START_PNL_DATA = {'Pnl': 0, 
                  'Cumulative Pnl' : 0, 
                  'Cash' : 0}
OPTIONS_LOG_FILE_PATH = 'OptionLogFile.txt'
Orders_LOG_FILE_PATH = 'OrdersLogFile.txt'
SAMPLE_OPTION_INSTRUMENT_PREFIX = 'BANKNIFTY1178375400'
EXP_DATE = '5/10/2017 15:30:00'
START_TIME = '5/3/2017 09:25:00'
CONTINUOS_SAVE_STATE_FILE_PREFIX = "saveState_"
HISTORY_CSV_FILE_PREFIX = "history/"
