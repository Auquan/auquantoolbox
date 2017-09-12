from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem


class PairExecutionSystem(SimpleExecutionSystem):
    def __init__(self, pair, pairRatio, pairEnter_threshold=0.7, pairExit_threshold=0.55, pairLongLimit=10, pairShortLimit=10, pairCapitalUsageLimit=0, pairLotSize=1):
        longLimit = {pair[0]: pairLongLimit, pair[1]: pairLongLimit * pairRatio}
        shortLimit = {pair[0]: pairShortLimit, pair[1]: pairShortLimit * pairRatio}
        lotSize = {pair[0]: pairLotSize, pair[1]: pairLotSize * pairRatio}
        super(PairExecutionSystem, self).__init__(enter_threshold=pairEnter_threshold,
                                                  exit_threshold=pairExit_threshold,
                                                  longLimit=longLimit,
                                                  shortLimit=shortLimit,
                                                  capitalUsageLimit=pairCapitalUsageLimit,
                                                  lotSize=lotSize)
