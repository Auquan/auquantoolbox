import useful_fn as utils


class Future:

	def __init__(self, futureVal, startDate, startTime):
		self.__futureVal = futureVal
		self.date = startDate
		self.time = startTime

    def getFutureVal(self):
    	return self.__futureVal

    def updateWithNewInstrument(self, futureInstrument):
    	self.date = futureInstrument.date
    	self.time = futureInstrument.time
    	self.__futureVal = futureInstrument.getVwap()
