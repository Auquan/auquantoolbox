from backtester.executionSystem.base_execution_system import BaseExecutionSystem, InstrumentExection
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.logger import *
import numpy as np
import pandas as pd


class Problem2ExecutionSystem(SimpleExecutionSystem):
    def __init__(self, enter_threshold=0.7, exit_threshold=0.55, longLimit=100,
                 shortLimit=100, capitalUsageLimit=0, enterlotSize=1, exitlotSize = 1, limitType='L', price='ask'):
        self.enter_threshold = enter_threshold
        self.exit_threshold = exit_threshold
        self.longLimit = longLimit
        self.shortLimit = shortLimit
        self.capitalUsageLimit = capitalUsageLimit
        self.enterlotSize = enterlotSize
        self.exitlotSize = exitlotSize
        self.limitType = limitType
        self.priceFeature = price

    def getPriceSeries(self, instrumentsManager):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        try:
            price = instrumentLookbackData.getFeatureDf(self.priceFeature).iloc[-1]
            return price
        except KeyError:
                logError('You have specified Dollar Limit but Price Feature Key %s does not exist'%self.priceFeature)

    def getInstrumentExecutionsFromExecutions(self, time, executions):
        instrumentExecutions = []
        for row in executions.iterrows():
            instrumentId = row[0]
            position = row[1]['position']
            price = row[1]['price']
            spread = row[1]['spread']
            instExecution = InstrumentExection(time=time,
                                               instrumentId=instrumentId,
                                               volume=np.abs(position),
                                               executionType=np.sign(position))
            setattr(instExecution, 'price', price)
            setattr(instExecution, 'spread', spread)

            instrumentExecutions.append(instExecution)
        return instrumentExecutions

    def getExecutions(self, time, instrumentsManager, capital):
        # import pdb;pdb.set_trace()
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        currentPredictions = instrumentLookbackData.getFeatureDf('prediction').iloc[-1]
        bidPriceSeries = self.getBidPrice(currentPredictions)
        askPriceSeries = self.getAskPrice(currentPredictions)

        positionData = instrumentLookbackData.getFeatureDf('position')
        position = positionData.iloc[-1]
        executions = pd.DataFrame(index=positionData.columns, columns=['position', 'price', 'spread'])
        executions['position'] = position
        executions['price'] = (bidPriceSeries + askPriceSeries)/2
        executions['spread'] = (askPriceSeries - bidPriceSeries)
        print('*********************** EXECUTIONS ***********************')
        print(executions)

        # executions is a df with stocknames as index and positions to execute and price as column (-10 means sell 10)
        # No executions if at position limit
        price = self.getPriceSeries(instrumentsManager)
        increasePosition = np.sign(position.T) == np.sign(executions)
        newPosition = position.T+executions
        executions[self.atPositionLimit(capital, newPosition, price, increasePosition)] = 0
        return self.getInstrumentExecutionsFromExecutions(time, executions)

    def getBidPrice(self, currentPredictions):
        return currentPredictions.apply(lambda tup: tup[0])

    def getAskPrice(self, currentPredictions):
        return currentPredictions.apply(lambda tup: tup[1])

    def getExecutionsAtClose(self, time, instrumentsManager):
        instrumentExecutions = []
        instruments = instrumentsManager.getAllInstrumentsByInstrumentId().values()
        for instrument in instruments:
            position = instrument.getCurrentPosition()
            if position == 0:
                continue
            instrumentExec = InstrumentExection(time=time,
                                                instrumentId=instrument.getInstrumentId(),
                                                volume=np.abs(position),
                                                executionType=-np.sign(position))
            instrumentExecutions.append(instrumentExec)
        return instrumentExecutions

    def exitPosition(self, time, instrumentsManager, currentPredictions, closeAllPositions=False):

        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()


        if closeAllPositions:
            executions['position'] = -position
            executions['price'] = bidPriceSeries
            executions['price'][executions['position']>0] = askPriceSeries
            return executions

        # executions[self.exitCondition(currentPredictions, instrumentsManager)] = -np.sign(position)*np.abs(position)
        # # print(executions)
        return executions

    def enterPosition(self, time, instrumentsManager, currentPredictions, capital):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getFeatureDf('position')
        position = positionData.iloc[-1]
        price = self.getPriceSeries(instrumentsManager)
        executions = pd.Series([0] * len(positionData.columns), index=positionData.columns)
        executions[self.enterCondition(currentPredictions, instrumentsManager)] = \
            self.getEnterLotSize(positionData.columns, price) * self.getBuySell(currentPredictions, instrumentsManager)
        # print(executions)
        return executions

    def getBuySell(self, currentPredictions, instrumentsManager):
        return np.sign(currentPredictions - 0.5)

    def enterCondition(self, currentPredictions, instrumentsManager):
        # print('Enter')
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        predictions = instrumentLookbackData.getFeatureDf('prediction')
        if len(predictions.index)>1:
            pastPredictions = instrumentLookbackData.getFeatureDf('prediction').iloc[-2]
        else:
            pastPredictions=currentPredictions.copy()
        # print((pastPredictions!=currentPredictions)&((currentPredictions - 0.5).abs() > (self.enter_threshold - 0.5)))
        return ((pastPredictions!=currentPredictions)&((currentPredictions - 0.5).abs() > (self.enter_threshold - 0.5)))

    def atPositionLimit(self, capital, position, price, increasePosition):

        if capital <= self.capitalUsageLimit:
            logWarn('Not Enough Capital')
            #TODO: Doesn't let you enter because it assumes enter always increases position. Fix this
            print(increasePosition)
            return increasePosition
        # TODO: Cant do this if position and getLongLimit indexes dont match
        return (position > self.getLongLimit(position.index, price)) | (position < -self.getShortLimit(position.index, price))

    def exitCondition(self, currentPredictions, instrumentsManager):
        # print('Exit')
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        predictions = instrumentLookbackData.getFeatureDf('prediction')
        if len(predictions.index)>1:
            pastPredictions = instrumentLookbackData.getFeatureDf('prediction').iloc[-2]
        else:
            pastPredictions=currentPredictions.copy()
        # print(pastPredictions!=currentPredictions)
        return pastPredictions!=currentPredictions
