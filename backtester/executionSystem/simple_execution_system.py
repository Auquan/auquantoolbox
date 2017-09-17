from backtester.executionSystem.base_execution_system import BaseExecutionSystem, InstrumentExection
from backtester.logger import *
import numpy as np


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

    def getLongLimit(self, instrument):
        instrumentId = instrument.getInstrumentId()
        if isinstance(self.longLimit, dict):
            return self.convertLimit(self.longLimit[instrumentId], instrument)
        else:
            return self.convertLimit(self.longLimit, instrument)

    def getShortLimit(self, instrument):
        instrumentId = instrument.getInstrumentId()
        if isinstance(self.shortLimit, dict):
            return self.convertLimit(self.shortLimit[instrumentId], instrument)
        else:
            return self.convertLimit(self.shortLimit, instrument)

    def getLotSize(self, instrument):
        instrumentId = instrument.getInstrumentId()
        if isinstance(self.lotSize, dict):
            return self.convertLimit(self.lotSize[instrumentId], instrument)
        else:
            return self.convertLimit(self.lotSize, instrument)

    def convertLimit(self, value, instrument):
        if self.limitType == 'L':
            return value
        try:
            price = instrument.getDataDf()[self.priceFeature].iloc[-1]
            return np.floor(np.float(value) / price)
        except KeyError:
            logError(
                'You have specified Dollar Limit but Price Feature Key does not exist')

    def getExecutions(self, time, instrumentsManager, capital):
        # TODO:
        marketFeaturesDf = instrumentsManager.getDataDf()
        currentMarketFeatures = marketFeaturesDf.iloc[-1]
        currentPredictions = marketFeaturesDf['prediction'].iloc[-1]
        logInfo(str(currentPredictions))
        executions = []
        executions += self.exitPosition(time, instrumentsManager, currentPredictions)
        executions += self.enterPosition(time, instrumentsManager,
                                         currentPredictions, capital)
        return executions

    def exitPosition(self, time, instrumentsManager, currentPredictions, closeAllPositions=False):
        executions = []
        instruments = instrumentsManager.getAllInstrumentsByInstrumentId().values()
        for instrument in instruments:
            position = instrument.getCurrentPosition()
            if position == 0:
                continue
            if closeAllPositions:
                instrumentExec = InstrumentExection(
                    time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
                executions.append(instrumentExec)
            # take Profits
            elif self.exitCondition(instrumentsManager, instrument, currentPredictions):
                instrumentExec = InstrumentExection(
                    time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
                executions.append(instrumentExec)
                logInfo('EXIT TRADE: %s Size: %.2f B/S: %i ' % (
                        instrument.getInstrumentId(), np.abs(position), -np.sign(position)))

            # hack
            elif self.hackCondition(instrumentsManager):
                instrumentExec = InstrumentExection(
                    time, instrument.getInstrumentId(), np.abs(position), -np.sign(position))
                executions.append(instrumentExec)
                logInfo('HACK TRADE: %s Size: %.2f B/S: %i ' % (
                        instrument.getInstrumentId(), np.abs(position), -np.sign(position)))
        return executions

    def enterPosition(self, time, instrumentsManager, currentPredictions, capital):
        executions = []
        for instrumentId in currentPredictions.keys():
            instrument = instrumentsManager.getInstrument(instrumentId)
            if instrument is None:
                continue
            # Dont add if already at limit
            if self.atPositionLimit(capital, instrumentsManager, instrument):
                continue
            # Enter position if condition met
            if self.enterCondition(instrumentsManager, instrument, currentPredictions):
                buySell = self.getBuySell(instrument, currentPredictions, instrumentsManager)
                logInfo('ENTER TRADE: %s Size: %.2f B/S: %i ' % (
                        instrumentId, self.getLotSize(instrument), buySell))
                instrumentExec = InstrumentExection(time, instrumentId,
                                                    self.getLotSize(instrument), buySell)
                executions.append(instrumentExec)
        return executions

    def getBuySell(self, instrument, currentPredictions, instrumentsManager):
        instrumentId = instrument.getInstrumentId()
        return np.sign(currentPredictions[instrumentId] - 0.5)

    def enterCondition(self, instrumentsManager, instrument, currentPredictions):
        instrumentId = instrument.getInstrumentId()
        probBuy = currentPredictions[instrumentId]
        return np.abs(probBuy - 0.5) > (self.enter_threshold - 0.5)

    def atPositionLimit(self, capital, instrumentsManager, instrument):
        position = instrument.getCurrentPosition()
        instrumentId = instrument.getInstrumentId()
        if (position > self.getLongLimit(instrument)) or (position < -self.getShortLimit(instrument)):
            logWarn('At Position Limit for %s' % instrumentId)
            return True
        if capital < self.capitalUsageLimit:
            logWarn('Not Enough Capital')
            return True
        return False

    def exitCondition(self, instrumentsManager, instrument, currentPredictions):
        instrumentId = instrument.getInstrumentId()
        probBuy = currentPredictions[instrumentId]
        return np.abs(probBuy - 0.5) < (self.exit_threshold - 0.5)

    def hackCondition(self, instrumentsManager):
        return False
