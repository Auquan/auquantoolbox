class InstrumentExection:
    def __init__(self, instrumentId, volumne, executionType):
        self.__instrumentId = instrumentId
        self.__volume = volumne
        self.__executionType = executionType

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
