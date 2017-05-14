class Future:

    def __init__(self, futureVal, startTime, position=0):
        self.__futureVal = futureVal
        self.time = startTime
        self.position = position

    def getFutureVal(self):
        return self.__futureVal

    def updateWithNewInstrument(self, futureInstrument):
        self.time = futureInstrument.time
        self.__futureVal = futureInstrument.getVwap()

    def updateWithOrder(self, order):
        self.position += order.volume
        self.__futureVal = order.tradePrice
