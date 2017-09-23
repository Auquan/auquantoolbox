from backtester.executionSystem.base_execution_system import BaseExecutionSystem, InstrumentExection
from backtester.logger import *
import numpy as np
import pandas as pd


class SimpleExecutionSystem(BaseExecutionSystem):
    def __init__(self, enter_threshold=0.7, exit_threshold=0.55, longLimit=10,
                 shortLimit=10, capitalUsageLimit=0, lotSize=1, limitType='L', price=''):
        self.enter_threshold = enter_threshold
        self.exit_threshold = exit_threshold
        self.longLimit = longLimit
        self.shortLimit = shortLimit
        self.capitalUsageLimit = capitalUsageLimit
        self.lotSize = lotSize
        self.limitType = limitType
        self.priceFeature = price

    def getLongLimit(self, instrumentIds):
        if isinstance(self.longLimit, pd.DataFrame):
            return self.convertLimit(self.longLimit)
        if isinstance(self.longLimit, dict):
            longLimitDf = pd.DataFrame(self.longLimit.values())
            return self.convertLimit(longLimitDf)
        else:
            return self.convertLimit(pd.Series(self.longLimit, index=instrumentIds))

    def getShortLimit(self, instrumentIds):
        if isinstance(self.shortLimit, pd.DataFrame):
            return self.convertLimit(self.shortLimit)
        if isinstance(self.shortLimit, dict):
            shortLimitDf = pd.DataFrame(self.shortLimit.values())
            return self.convertLimit(shortLimitDf)
        else:
            return self.convertLimit(pd.Series(self.shortLimit, index=instrumentIds))

    def getLotSize(self, instrumentIds):
        if isinstance(self.lotSize, pd.DataFrame):
            return self.convertLimit(self.lotSize)
        if isinstance(self.lotSize, dict):
            lotSizeDf = pd.DataFrame(self.lotSize.values())
            return self.convertLimit(lotSizeDf)
        else:
            return self.convertLimit(pd.Series(self.lotSize, index=instrumentIds))

    def convertLimit(self, df):
        if self.limitType == 'L':
            return df
        return NotImplementedError
        # TODO Support this
        # try:
        #     price = instrument.getDataDf()[self.priceFeature].iloc[-1]
        #     return np.floor(np.float(value) / price)
        # except KeyError:
        #     logError(
        #         'You have specified Dollar Limit but Price Feature Key does not exist')

    def getInstrumentExecutionsFromExecutions(self, time, executions):
        instrumentExecutions = []
        for (instrumentId, position) in executions.iteritems():
            if position == 0:
                continue
            instExecution = InstrumentExection(time=time,
                                               instrumentId=instrumentId,
                                               volume=np.abs(position),
                                               executionType=np.sign(position))
            instrumentExecutions.append(instExecution)
        return instrumentExecutions

    def getExecutions(self, time, instrumentsManager, capital):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        currentPredictions = instrumentLookbackData.getFeatureDf('prediction').iloc[-1]
        executions = self.exitPosition(time, instrumentsManager, currentPredictions)
        executions += self.enterPosition(time, instrumentsManager, currentPredictions, capital)
        # executions is a series with stocknames as index and positions to execute as column (-10 means sell 10)
        return self.getInstrumentExecutionsFromExecutions(time, executions)

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
        positionData = instrumentLookbackData.getFeatureDf('position')
        position = positionData.iloc[-1]
        executions = pd.Series([0] * len(positionData.columns), index=positionData.columns)

        if closeAllPositions:
            executions = -position
            return executions
        executions[self.exitCondition(currentPredictions, instrumentsManager)] = -position
        executions[self.hackCondition(currentPredictions, instrumentsManager)] = -position

        return executions

    def enterPosition(self, time, instrumentsManager, currentPredictions, capital):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getFeatureDf('position')
        position = positionData.iloc[-1]
        executions = pd.Series([0] * len(positionData.columns), index=positionData.columns)
        executions[self.enterCondition(currentPredictions, instrumentsManager)] = \
            self.getLotSize(positionData.columns) * self.getBuySell(currentPredictions, instrumentsManager)
        # No executions if at position limit
        executions[self.atPositionLimit(capital, positionData)] = 0

        return executions

    def getBuySell(self, currentPredictions, instrumentsManager):
        return np.sign(currentPredictions - 0.5)

    def enterCondition(self, currentPredictions, instrumentsManager):

        return (currentPredictions - 0.5).abs() > (self.enter_threshold - 0.5)

    def atPositionLimit(self, capital, positionData):
        if capital < self.capitalUsageLimit:
            logWarn('Not Enough Capital')
            return pd.Series(True, index=positionData.columns)
        position = positionData.iloc[-1]
        return (position > self.getLongLimit(positionData.columns)) | (position < -self.getShortLimit(positionData.columns))

    def exitCondition(self, currentPredictions, instrumentsManager):
        return (currentPredictions - 0.5).abs() < (self.exit_threshold - 0.5)

    def hackCondition(self, currentPredictions, instrumentsManager):
        return pd.Series(False, index=currentPredictions.index)
