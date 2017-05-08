class Future:

    def __init__(self, futureVal, startTime):
        self.__futureVal = futureVal
        self.time = startTime

    def getFutureVal(self):
        return self.__futureVal

    def updateWithNewInstrument(self, futureInstrument):
        self.time = futureInstrument.time
        self.__futureVal = futureInstrument.getVwap()
