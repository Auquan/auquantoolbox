from base_execution_system import BaseExecutionSystem, InstrumentExection


class SimpleExecutionSystem(BaseExecutionSystem):
    def __init__(self, longLimit, shortLimit):
        self.__longLimit = longLimit
        self.__shortLimit = shortLimit

    def getExecutions(self, time, instrumentsManager):
        # TODO:
        return []
