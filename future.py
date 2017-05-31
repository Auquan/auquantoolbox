class Future:

    def __init__(self, futureVal, roll, startTime, position=0):
        self.__futureVal = futureVal
        self.roll = 0
        self.time = startTime
        self.position = position

    def getFutureVal(self):
        return self.__futureVal

    def updateWithNewInstrument(self, futureInstrument):
        self.time = futureInstrument.time
        self.__futureVal = futureInstrument.getVwap()

    def updateWithOrder(self, order):
        self.position += order.volume

    def updateRoll(self, newRoll):
        self.roll = newRoll

    def getRoll(self):
        return self.roll
