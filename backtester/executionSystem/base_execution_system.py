class InstrumentExection:
    def __init__(self, time, instrumentId, volume, executionType):
        self.__timeOfExecution = time
        self.__instrumentId = instrumentId
        self.__volume = volume
        self.__executionType = executionType

    def getTimeOfExecution(self):
        return self.__timeOfExecution

    def getInstrumentId(self):
        return self.__instrumentId

    def getVolume(self):
        return self.__volume

    def getExecutionType(self):
        return self.__executionType


class BaseExecutionSystem(object):

    '''
    Returns an array of InstrumentExecutions
    '''
    def getExecutions(self, time, instrumentsManager, capital):
        return []

    def getExecutionsAtClose(self, time, instrumentsManager):
        return []
