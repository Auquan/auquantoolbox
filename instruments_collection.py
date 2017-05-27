class InstrumentCollection:
    def __init__(self):
        self.__instrumentsDict = {}

    def getInstrument(self, instrumentId):
        return self.instrumentsDict[instrumentId]
