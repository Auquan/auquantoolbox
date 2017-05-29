import math
from datetime import datetime
import instrument
import pandas as pd
import order
from constants import *

TYPE_LINE_UNDEFINED = 0
TYPE_LINE_BOOK_DATA = 1
TYPE_LINE_GREEK = 2  # not used anymore
TYPE_LINE_BOOK_OPTION = 3


def checkDate(lineItem):
    try:
        datetime.strptime(lineItem, '%Y/%m/%d')
        return True
    except ValueError:
        return False


def checkTimestamp(lineItem):
    return True


# Returns the type of lineItems
def validateLineItem(lineItems):
    if len(lineItems) < 4:
        return TYPE_LINE_UNDEFINED
    if checkDate(lineItems[0]) and checkTimestamp(lineItems[1]) and lineItems[2] == "Book":
        return TYPE_LINE_BOOK_DATA
    if checkDate(lineItems[0]) and checkTimestamp(lineItems[1]) and lineItems[2] == "Greek:":
        return TYPE_LINE_GREEK
    if len(lineItems) == 7 and lineItems[3] == '|':
        return TYPE_LINE_BOOK_OPTION
    return TYPE_LINE_UNDEFINED


def parseGreekLine(line):
    parsedGreekLine = {}
    line = line.replace("ref_fut_px :", "ref_fut_px:")
    lineItems = line.split()
    parsedGreekLine['date'] = lineItems[0]
    parsedGreekLine['ts'] = lineItems[1]
    lineItems = lineItems[3:]
    i = 0
    while (i < len(lineItems)):
        parsedGreekLine[lineItems[i]] = lineItems[i + 1]
        i = i + 2
    return parsedGreekLine


def parseBookDataLineItems(lineItems):
    symbol = lineItems[4]
    return symbol


def parseSymbolFromBookDataLineItems(lineItems):
    symbol = lineItems[4]
    return symbol

# returns the minute time when this data was logged


def parseTimestampFromBookDataLineItems(lineItems):
    exactTimestampStr = lineItems[1]
    tsComponents = exactTimestampStr.split(':')
    return tsComponents[0] + ':' + tsComponents[1] + ':' + tsComponents[2] + ':000000'


def parseBookDataOptionLine(lineItems):
    if (len(lineItems) < 7):
        return None
    bidVol = float(lineItems[1])
    bidPrice = float(lineItems[2])
    askPrice = float(lineItems[4])
    askVol = float(lineItems[5])
    return [bidVol, bidPrice, askPrice, askVol]


def convertStrikeToSymbol(strike, optionRef, isCall):
    callStr = "004"
    if isCall:
        callStr = "003"
    return optionRef[:-len(str(strike) + callStr)] + str(strike) + callStr


def get_vwap(bid_vol, bid_price, ask_price, ask_vol):
    try:
        price = (float(bid_price) * float(ask_vol) + float(ask_price) * float(bid_vol)) / \
            (float(bid_vol) + float(ask_vol)) / \
            100  # Calculated for a vol = 0.12353
    except ZeroDivisionError:
        price = (float(bid_price) + float(ask_price)) / 200
    return price

# trasnforms data we collected to the format that it needs to be returned


def transformTimestampData(timestampData, futureSymbol, optionRef):
    if not (futureSymbol in timestampData):
        return timestampData

    futureOptionData = timestampData[futureSymbol]
    futureVal = get_vwap(futureOptionData['bidVol'], futureOptionData[
                         'bidPrice'], futureOptionData['askPrice'], futureOptionData['askVol'])
    timestampData['future'] = futureVal
    lowFuture = int(math.floor(futureVal / 100.0)) * 100
    highFuture = int(math.ceil(futureVal / 100.0)) * 100
    lowFutureCallSymbol = convertStrikeToSymbol(lowFuture, optionRef, True)
    lowFuturePutSymbol = convertStrikeToSymbol(lowFuture, optionRef, False)
    highFutureCallSymbol = convertStrikeToSymbol(highFuture, optionRef, True)
    highFuturePutSymbol = convertStrikeToSymbol(highFuture, optionRef, False)

    try:
        lowOptionsCallData = timestampData[lowFutureCallSymbol]
        lowOptionsPutData = timestampData[lowFuturePutSymbol]
        highOptionsCallData = timestampData[highFutureCallSymbol]
        highOptionsPutData = timestampData[highFuturePutSymbol]

        timestampData['C0'] = lowOptionsCallData
        timestampData['C0']['strike'] = lowFuture
        timestampData['P0'] = lowOptionsPutData
        timestampData['P0']['strike'] = lowFuture
        timestampData['C1'] = highOptionsCallData
        timestampData['C1']['strike'] = highFuture
        timestampData['P1'] = highOptionsPutData
        timestampData['P1']['strike'] = highFuture
    except:
        print('badddd data')
    print(timestampData)
    return timestampData


# given a file name
# returns an array of timestamp data [timestampData]
# timestampData has following keys
# time, future, C0, C1, P0, P1 as before
# also has for that time all the other options values too. The key is the symbol
# sample timestampData
'''
{'BANKNIFTY115297380018400003': {'strike': 18400, 'askVol': '40', 'bidVol': '40', 'bidPrice': '5445.0000000', 'askPrice': '5560.0000000'},
'BANKNIFTY115297380018800004': {'askVol': '0', 'bidVol': '0', 'bidPrice': '0.0000000', 'askPrice': '0.0000000'},
'BANKNIFTY115297380018800003': {'askVol': '1800', 'bidVol': '120', 'bidPrice': '220.0000000', 'askPrice': '505.0000000'},
'BANKNIFTY115297380018400004': {'strike': 18400, 'askVol': '40', 'bidVol': '40', 'bidPrice': '11510.0000000', 'askPrice': '13430.0000000'},
'BANKNIFTY115297380018100003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '24040.0000000', 'askPrice': '24300.0000000'},
'BANKNIFTY115297380018100004': {'askVol': '200', 'bidVol': '80', 'bidPrice': '2410.0000000', 'askPrice': '2540.0000000'},
'BANKNIFTY115297380018300004': {'strike': 18300, 'askVol': '320', 'bidVol': '360', 'bidPrice': '7115.0000000', 'askPrice': '7700.0000000'},
'BANKNIFTY115297380018300003': {'strike': 18300, 'askVol': '40', 'bidVol': '40', 'bidPrice': '9850.0000000', 'askPrice': '9990.0000000'},
'BANKNIFTY115297380017400003': {'askVol': '0', 'bidVol': '0', 'bidPrice': '0.0000000', 'askPrice': '0.0000000'},
'BANKNIFTY115297380019100003': {'askVol': '0', 'bidVol': '0', 'bidPrice': '0.0000000', 'askPrice': '0.0000000'},
'BANKNIFTY115297380017700003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '59285.0000000', 'askPrice': '74550.0000000'},
'BANKNIFTY115297380017700004': {'askVol': '680', 'bidVol': '2360', 'bidPrice': '385.0000000', 'askPrice': '400.0000000'},
'BANKNIFTY115297380017800003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '50200.0000000', 'askPrice': '53440.0000000'},
'BANKNIFTY115297380017800004': {'askVol': '40', 'bidVol': '40', 'bidPrice': '590.0000000', 'askPrice': '610.0000000'},
'BANKNIFTY115297380017600003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '3515.0000000', 'askPrice': '84520.0000000'},
'BANKNIFTY115297380018500004': {'askVol': '80', 'bidVol': '40', 'bidPrice': '18060.0000000', 'askPrice': '19495.0000000'},
 'BANKNIFTY115297380018000004': {'askVol': '360', 'bidVol': '40', 'bidPrice': '1350.0000000', 'askPrice': '1470.0000000'},
 'C0': {'strike': 18300, 'askVol': '40', 'bidVol': '40', 'bidPrice': '9850.0000000', 'askPrice': '9990.0000000'},
 'BANKNIFTY115297380018000003': {'askVol': '40', 'bidVol': '400', 'bidPrice': '33300.0000000', 'askPrice': '33565.0000000'},
 'BANKNIFTY115297380018500003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '2645.0000000', 'askPrice': '2695.0000000'},
 'BANKNIFTY115297380017600004': {'askVol': '40', 'bidVol': '200', 'bidPrice': '220.0000000', 'askPrice': '270.0000000'},
 'P0': {'strike': 18300, 'askVol': '320', 'bidVol': '360', 'bidPrice': '7115.0000000', 'askPrice': '7700.0000000'},
 'P1': {'strike': 18400, 'askVol': '40', 'bidVol': '40', 'bidPrice': '11510.0000000', 'askPrice': '13430.0000000'},
 'BANKNIFTY115297380018600003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '1115.0000000', 'askPrice': '1270.0000000'},
 'BANKNIFTY115297380018600004': {'askVol': '0', 'bidVol': '0', 'bidPrice': '0.0000000', 'askPrice': '0.0000000'},
  'BANKNIFTY115297380018900003': {'askVol': '2400', 'bidVol': '1000', 'bidPrice': '5.0000000', 'askPrice': '500.0000000'},
  'BANKNIFTY115297380019000003': {'askVol': '400', 'bidVol': '80', 'bidPrice': '75.0000000', 'askPrice': '130.0000000'},
  'BANKNIFTY115297380018700003': {'askVol': '40', 'bidVol': '200', 'bidPrice': '620.0000000', 'askPrice': '695.0000000'},
  'BANKNIFTY1154183400-10': {'askVol': '40', 'bidVol': '320', 'bidPrice': '1835700.0000000', 'askPrice': '1835800.0000000'},
  'C1': {'strike': 18400, 'askVol': '40', 'bidVol': '40', 'bidPrice': '5445.0000000', 'askPrice': '5560.0000000'},
  'BANKNIFTY115297380018700004': {'askVol': '0', 'bidVol': '0', 'bidPrice': '0.0000000', 'askPrice': '0.0000000'},
  'BANKNIFTY115297380018200004': {'askVol': '160', 'bidVol': '80', 'bidPrice': '4160.0000000', 'askPrice': '4440.0000000'},
  'BANKNIFTY115297380017500003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '1670.0000000', 'askPrice': '100520.0000000'},
  'BANKNIFTY115297380017900004': {'askVol': '40', 'bidVol': '40', 'bidPrice': '855.0000000', 'askPrice': '870.0000000'},
  'BANKNIFTY115297380017900003': {'askVol': '40', 'bidVol': '40', 'bidPrice': '40560.0000000', 'askPrice': '53430.0000000'},
  'BANKNIFTY115297380017500004': {'askVol': '840', 'bidVol': '40', 'bidPrice': '160.0000000', 'askPrice': '195.0000000'},
   'BANKNIFTY115297380018200003': {'askVol': '40', 'bidVol': '320', 'bidPrice': '16025.0000000', 'askPrice': '16220.0000000'},
    'future': 18357.88888888889,
    'time': '09:17:00:000000'}
'''


def loadData(fileName):
    futureSymbol = None
    optionRef = None
    with open(fileName, "r") as f:
        accumulatedData = []
        currentTimestampData = {}
        currentTs = ''
        currentBookSymbol = ''

        for line in f:
            lineItems = line.split()
            lineItemType = validateLineItem(lineItems)

            if (lineItemType == TYPE_LINE_BOOK_DATA):
                tsOfData = parseTimestampFromBookDataLineItems(lineItems)
                if (tsOfData != currentTs):
                    # new time encountered, so add the previous one first and
                    # then clear data for new ts
                    accumulatedData.append(transformTimestampData(
                        currentTimestampData, futureSymbol, optionRef))
                    currentTs = tsOfData
                    currentTimestampData = {}
                    currentTimestampData['time'] = currentTs
                # resume to normal business
                currentBookSymbol = parseSymbolFromBookDataLineItems(lineItems)
            elif(lineItemType == TYPE_LINE_BOOK_OPTION):
                parsedOption = parseBookDataOptionLine(lineItems)
                if parsedOption and (not currentBookSymbol in currentTimestampData):
                    # just adding the first one only
                    currentTimestampData[currentBookSymbol] = parsedOption
            elif(lineItemType == TYPE_LINE_UNDEFINED):
                if (lineItems[0] == 'Interested') and (lineItems[1] == 'symbols'):
                    if (not futureSymbol):
                        futureSymbol = lineItems[3]
                    elif (not optionRef):
                        optionRef = lineItems[3]

        accumulatedData.append(transformTimestampData(
            currentTimestampData, futureSymbol, optionRef))  # add last missing data
        print(accumulatedData)
        return accumulatedData


class Dataparser:
    def __init__(self):
        self.currentTime = ''
        self.currentDate = ''
        self.currentInstrumentId = None
        self.currentBookData = []

    def processLines(self, lines):
        accumulatedInstruments = []
        for line in lines:
            lineItems = line.split()
            lineItemType = validateLineItem(lineItems)

            if (lineItemType == TYPE_LINE_BOOK_DATA):
                if self.currentInstrumentId is not None:
                    inst = instrument.Instrument(time=self.currentTime,
                                                 date=self.currentDate,
                                                 instrumentId=self.currentInstrumentId,
                                                 bookData=pd.DataFrame(self.currentBookData, columns=['bidVol', 'bidPrice', 'askPrice', 'askVol']))
                    accumulatedInstruments.append(inst)
                self.currentDate = lineItems[0]
                self.currentTime = lineItems[1]
                self.currentInstrumentId = lineItems[4][len(SAMPLE_OPTION_INSTRUMENT_PREFIX):]
                self.currentBookData = []
            elif(lineItemType == TYPE_LINE_BOOK_OPTION):
                parsedOption = parseBookDataOptionLine(lineItems)
                self.currentBookData.append(parsedOption)
        return accumulatedInstruments


class OrdersParser:

    def parseOrderFromLineItems(self, lineItems):
        instrumentId = lineItems[4][len(SAMPLE_OPTION_INSTRUMENT_PREFIX):]
        type = lineItems[6]
        volume = float(lineItems[10])
        volume = volume if type == 'BUY' else -volume
        tradePrice = float(lineItems[12])
        time = str(datetime.now())
        fees = 0.001 * tradePrice
        return order.Order(instrumentId=instrumentId, tradePrice=tradePrice, vol=volume, time=time, fees=fees)

    def processLines(self, lines):
        accumulatedOrders = []
        # :15:28:40.599762 NONE OrderSender::onFill:  symbol: BANKNIFTY118018980022600004 dir: BUY orderid: 3000011 fill_size: 80 fill_px: 12355 sent_px: 12380
        for line in lines:
            lineItems = line.split()
            if len(lineItems) < 3:
                continue
            if 'onFill' not in lineItems[2]:
                continue
            parsedOrder = self.parseOrderFromLineItems(lineItems)
            accumulatedOrders.append(parsedOrder)
        return accumulatedOrders


if __name__ == '__main__':
    d = loadData("test.txt")
