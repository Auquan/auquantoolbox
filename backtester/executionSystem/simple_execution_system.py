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

    def getExecutions(self, time, instrumentsManager, capital):
        # TODO:
        marketFeaturesDf = instrumentsManager.getDataDf()
        currentMarketFeatures = marketFeaturesDf.iloc[-1]
        predictionDict = marketFeaturesDf['prediction'].iloc[-1]
        currentPredictions = pd.DataFrame(predictionDict.values(), index=predictionDict.keys())
        logInfo(str(currentPredictions))
        import pdb
        pdb.set_trace()
        # executions = []
        executions = self.exitPosition(time, instrumentsManager, currentPredictions)
        executions += self.enterPosition(time, instrumentsManager, currentPredictions, capital)
        # executions is a series with stocknames as index and positions to execute as column (-10 means sell 10)
        return executions

    def exitPosition(self, time, instrumentsManager, currentPredictions, closeAllPositions=False):

        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        position = instrumentLookbackData.getDataForFeatureForAllInstruments('position').iloc[-1]
        executions = position * 0

        if closeAllPositions:
            executions = -position
            return executions
        executions[self.exitCondition(currentPredictions, instrumentsManager)] = -position
        executions[self.hackCondition(currentPredictions, instrumentsManager)] = -position

        # executions = []

        # for instrument in instruments:
        #     position = instrument.getCurrentPosition()
        #     if position == 0:
        #         continue
        #     if closeAllPositions:
        #         instrumentExec = InstrumentExection(
        #             time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
        #         executions.append(instrumentExec)
        #     # take Profits
        #     elif self.exitCondition(instrumentsManager, instrument, currentPredictions):
        #         instrumentExec = InstrumentExection(
        #             time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
        #         executions.append(instrumentExec)
        #         logInfo('EXIT TRADE: %s Size: %.2f B/S: %i ' % (
        #                 instrument.getInstrumentId(), np.abs(position), -np.sign(position)))

        #     # hack
        #     elif self.hackCondition(instrumentsManager):
        #         instrumentExec = InstrumentExection(
        #             time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
        #         executions.append(instrumentExec)
        #         logInfo('HACK TRADE: %s Size: %.2f B/S: %i ' % (
        #                 instrument.getInstrumentId(), np.abs(position), -np.sign(position)))
        return executions

    def enterPosition(self, time, instrumentsManager, currentPredictions, capital):
        instrumentLookbackData = instrumentsManager.getLookbackInstrumentFeatures()
        position = instrumentLookbackData.getDataForFeatureForAllInstruments('position')
        executions = position * 0
        executions[self.enterCondition(currentPredictions, instrumentsManager)] = \
            self.getLotSize(position.columns) * self.getBuySell(currentPredictions, instrumentsManager)
        # No executions if at position limit
        executions[self.atPositionLimit(capital, position)] = 0
        # for instrumentId in currentPredictions.keys():
        #     instrument = instrumentsManager.getInstrument(instrumentId)
        #     if instrument is None:
        #         continue
        #     # Dont add if already at limit
        #     if self.atPositionLimit(capital, instrumentsManager, instrument):
        #         continue
        #     # Enter position if condition met
        #     if self.enterCondition(instrumentsManager, instrument, currentPredictions):
        #         buySell = self.getBuySell(instrument, currentPredictions, instrumentsManager)
        #         logInfo('ENTER TRADE: %s Size: %.2f B/S: %i ' % (
        #                 instrumentId, self.getLotSize(instrument), buySell))
        #         instrumentExec = InstrumentExection(time, instrumentId,
        #                                             self.getLotSize(instrument), buySell)
        #         executions.append(instrumentExec)
        return executions

    def getBuySell(self, currentPredictions, instrumentsManager):
        # instrumentId = instrument.getInstrumentId()
        # return np.sign(currentPredictions[instrumentId] - 0.5)
        return np.sign(currentPredictions - 0.5)

    def enterCondition(self, currentPredictions, instrumentsManager):
        # instrumentId = instrument.getInstrumentId()
        # probBuy = currentPredictions[instrumentId]
        # return np.abs(probBuy - 0.5) > (self.enter_threshold - 0.5)
        return (currentPredictions - 0.5).abs() > (self.enter_threshold - 0.5)

    def atPositionLimit(self, capital, position):
        # position = instrument.getCurrentPosition()
        # instrumentId = instrument.getInstrumentId()
        # if (position > self.getLongLimit(instrument)) or (position < -self.getShortLimit(instrument)):
        #     logWarn('At Position Limit for %s' % instrumentId)
        #     return True
        if capital < self.capitalUsageLimit:
            logWarn('Not Enough Capital')
            return pd.Series(True, index=currentPredictions.index)
        return (position > self.getLongLimit(position.columns)) | (position < -self.getShortLimit(position.columns))

    def exitCondition(self, currentPredictions, instrumentsManager):
        # instrumentId = instrument.getInstrumentId()
        # probBuy = currentPredictions[instrumentId]
        # return np.abs(probBuy - 0.5) < (self.exit_threshold - 0.5)
        return (currentPredictions - 0.5).abs() < (self.exit_threshold - 0.5)

    def hackCondition(self, currentPredictions):
        return pd.Series(False, index=currentPredictions.index)
