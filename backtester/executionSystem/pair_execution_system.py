from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.logger import *
import pandas as pd


class PairExecutionSystem(SimpleExecutionSystem):
    def __init__(self, pair, pairRatio, pairEnter_threshold=0.7, pairExit_threshold=0.55, pairLongLimit=10, pairShortLimit=10, pairCapitalUsageLimit=0, pairLotSize=1, price=None):
        try:
            longLimit = {pair[0]: pairLongLimit, pair[1]: pairLongLimit * pairRatio}
            shortLimit = {pair[0]: pairShortLimit, pair[1]: pairShortLimit * pairRatio}
            lotSize = {pair[0]: pairLotSize, pair[1]: pairLotSize * pairRatio}
            super(PairExecutionSystem, self).__init__(enter_threshold=pairEnter_threshold,
                                                      exit_threshold=pairExit_threshold,
                                                      longLimit=longLimit,
                                                      shortLimit=shortLimit,
                                                      capitalUsageLimit=pairCapitalUsageLimit,
                                                      enterlotSize=lotSize,
                                                      exitlotSize=lotSize,
                                                      price = price)
        except IndexError:
            logError("The pair does not have exactly two elements")
    def getExecutions(self, time, instrumentsManager, capital):
        marketFeatures = instrumentsManager.getLookbackMarketFeatures().getData()
        try:
            currentPrediction = marketFeatures['prediction'].iloc[-1]
            currentPredictions = pd.DataFrame(data=[currentPrediction], index=[time]).iloc[-1]
            executions = self.exitPosition(time, instrumentsManager, currentPredictions)
            executions += self.enterPosition(time, instrumentsManager, currentPredictions, capital)
            # executions is a series with stocknames as index and positions to execute as column (-10 means sell 10)
            return self.getInstrumentExecutionsFromExecutions(time, executions)
        except IndexError:
            logError("DataFrame is empty")
        # TODO: Error shown while giving a dataframe with more than 2 columns
        except ValueError:
            logError("The DataFrames does not have exactly 2 columns")
