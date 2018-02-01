''' demonstrate the pydispatch module '''
from pydispatch import dispatcher
import threading
import time
import datetime
from backtester.dataSource.alpha_grep_data_source import AlphaGrepDataSource


DATASOURCE_SIGNAL='datasource_signal'
DATASOURCE_SENDER='datasource_sender'
DATA_SIGNAL='data_signal'
DATA_SENDER='data_sender'

class InstrumentData():
    def __init__(self, symbol, stock_bid_price, stock_bid_volume, stock_ask_price, stock_ask_volume, future_bid_price, future_bid_volume, future_ask_price, future_ask_volume):
        # TODO support all 5 levels of data
        self.symbol = symbol
        self.stock_bid_price = stock_bid_price
        self.stock_bid_volume = stock_bid_volume
        self.stock_ask_price = stock_ask_price
        self.stock_ask_volume = stock_ask_volume
        self.future_bid_price = future_bid_price
        self.future_bid_volume = future_bid_volume
        self.future_ask_price = future_ask_price
        self.future_ask_volume = future_ask_volume

    def updateData(self, updateType, bid_price, bid_volume, ask_price, ask_volume):
        if(updateType == 'S'):
            self.stock_bid_price = bid_price
            self.stock_bid_volume = bid_volume
            self.stock_ask_price = ask_price
            self.stock_ask_volume = ask_volume
        elif(updateType == 'F'):
            self.future_bid_price = bid_price
            self.future_bid_volume = bid_volume
            self.future_ask_price = ask_price
            self.future_ask_volume = ask_volume

class InstrumentsInitializer():
    def __init__(self):
        # TODO add the full list, read from a stocklist file?
        self.instruments = ['HDFCBANK', 'BHARTIART', 'NIFTY', 'BANKNIFTY', 'JPASSOCIAT', 'GMRINFRA', 'ASHOKLEY']

    def initialize(self):
        # TODO have the close prices to initialize with everyday
        instrument_data_hash = {}

        for instrument in self.instruments:
            instrument_data_hash[instrument] = InstrumentData(instrument, 0, 0, 0, 0, 0, 0, 0, 0)

        return instrument_data_hash

class DataSource():
    def __init__(self):
        print('datasource instantiated')
        self.update = False
        self.instrument_updates = InstrumentsInitializer().initialize()
        dispatcher.connect(self.datasource_dispatcher_receive, signal=DATA_SIGNAL, sender=DATA_SENDER)
        self.emitInstrumentUpdates()

    def datasource_dispatcher_receive(self, message):
        ''' handle dispatcher'''
        #print('datasource has received message: {}'.format(message))
        print 'Update Received\n'
        self.instrument_updates[message['symbol']].updateData(message['update_type'], message['bid_price'], message['bid_volume'], message['ask_price'], message['ask_volume'])
        self.update = True

    def emitInstrumentUpdates(self):
        ''' loop and yield '''
        while(1):
            if(self.update):
                self.update = False
                print 'Update Received\n'
                print self.instrument_updates.values()[0].symbol
                print self.instrument_updates.values()[0].stock_bid_price
                print '\n'
                print self.instrument_updates.values()[1].symbol
                print self.instrument_updates.values()[1].stock_bid_price
                print '\n'
                print self.instrument_updates.values()[2].symbol
                print self.instrument_updates.values()[2].stock_bid_price
                print '\n'
                print self.instrument_updates.values()[3].symbol
                print self.instrument_updates.values()[3].stock_bid_price
                print '\n'
                print self.instrument_updates.values()[4].symbol
                print self.instrument_updates.values()[4].stock_bid_price
                print '\n'
                #yield([datetime.datetime.now(), self.instrument_updates.values()])

if __name__ == '__main__':
        data_thread = threading.Thread(target=DataSource)
        data_thread.start()
        sender_thread = threading.Thread(target=AlphaGrepDataSource)
        sender_thread.start()
