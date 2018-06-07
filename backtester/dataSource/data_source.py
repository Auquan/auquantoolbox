import pandas as pd

class DataSource(object):
    # emits list of instrument updates at the same time.
    # The caller needs to ensure all these updates are happening at the same time
    # emits [t1, [i1, i2, i3]], where i1, i2, i3 are updates happening at time t1
    def emitInstrumentUpdates(self):
        raise NotImplementedError

    # returns a list of instrument identifiers
    def getInstrumentIds(self):
        raise NotImplementedError

    # returns a list of feature keys which are already present in the data.
    def getBookDataFeatures(self):
        raise NotImplementedError

    def processAllInstrumentUpdates_v1(self):
        frames = {instrumentId : [] for instrumentId in self.getInstrumentIds()}
        for timeOfUpdate, instrumentUpdates in self.emitInstrumentUpdates():
            for instrumentUpdate in instrumentUpdates:
                frames[instrumentUpdate.getInstrumentId()].append(pd.DataFrame([instrumentUpdate.getBookData()],
                                                                                index=[timeOfUpdate]))
        # del self.__groupedInstrumentUpdates
        self.__instrumentDataDict = {inst : pd.concat(frames[inst]) if frames[inst] else None for inst in self.getInstrumentIds()}

    def processAllInstrumentUpdates_v2(self):
        instrumentUpdateFlag = {instrumentId : False for instrumentId in self.getInstrumentIds()}
        self.__instrumentDataDict = {instrumentId : pd.DataFrame(index=self.getAllTimes()) for instrumentId in self.getInstrumentIds()}
        lastTimeOfUpdate = None
        for timeOfUpdate, instrumentUpdates in self.emitInstrumentUpdates():
            for instrumentUpdate in instrumentUpdates:
                instrumentId = instrumentUpdate.getInstrumentId()
                instrumentUpdateFlag[instrumentId] = True
                for col in instrumentUpdate.getBookData():
                    self.__instrumentDataDict[instrumentId].at[timeOfUpdate, col] = instrumentUpdate.getBookData()[col]
            for instrumentId in instrumentUpdateFlag:
                if (not instrumentUpdateFlag[instrumentId]) and (lastTimeOfUpdate is not None):
                    self.__instrumentDataDict[instrumentId].at[timeOfUpdate, :] = self.__instrumentDataDict[instrumentId].loc[lastTimeOfUpdate].values
                instrumentUpdateFlag[instrumentId] = False
            lastTimeOfUpdate = timeOfUpdate
        for instrumentId in self.__instrumentDataDict:
            self.__instrumentDataDict[instrumentId].fillna(0.0, inplace=True)

    # accretes all instrument updates using emitInstrumentUpdates method
    def processAllInstrumentUpdates(self, pad=True):
        self.__instrumentDataDict = {instrumentId : pd.DataFrame(index=self.getAllTimes()) for instrumentId in self.getInstrumentIds()}
        for timeOfUpdate, instrumentUpdates in self.emitInstrumentUpdates():
            for instrumentUpdate in instrumentUpdates:
                instrumentId = instrumentUpdate.getInstrumentId()
                for col in instrumentUpdate.getBookData():
                    self.__instrumentDataDict[instrumentId].at[timeOfUpdate, col] = instrumentUpdate.getBookData()[col]
        for instrumentId in self.__instrumentDataDict:
            if pad:
                self.__instrumentDataDict[instrumentId].fillna(method='ffill', inplace=True)
                self.__instrumentDataDict[instrumentId].fillna(0.0, inplace=True)
            else:
                self.__instrumentDataDict[instrumentId].dropna(inplace=True)


    # emits the dict of all instrument updates where
    # keys are instrumentId and values are pandas dataframe
    def emitAllInstrumentUpdates(self):
        ## stock wise data
        # for instrumentId in self.getInstrumentIds():
            # yield self.__instrumentDataDict[instrumentId]
        return self.__instrumentDataDict

    # selects only those instrument updates which lie within dateRange
    def filterUpdatesByDates(self, dateRange=None):
        dateRange = dateRange if dateRange else (self.__startDateStr, self.__endDateStr)
        for instrumentId in self.getInstrumentIds():
            if type(dateRange) is list and self.__instrumentDataDict[instrumentId] is not None:
                frames = []
                for dr in dateRange:
                    frames.append(self.__instrumentDataDict[instrumentId][dr[0]:dr[1]])
                self.__instrumentDataDict[instrumentId] = pd.concat(frames)
            elif self.__instrumentDataDict[instrumentId] is not None:
                self.__instrumentDataDict[instrumentId] = self.__instrumentDataDict[instrumentId][dateRange[0]:dateRange[1]]

    def setStartDate(self, startDateStr):
        self.__startDateStr = startDateStr

    def setEndDate(self, endDateStr):
        self.__endDateStr = endDateStr

    def setDateRange(self, dateRange):
        self.__dateRange = dateRange

    '''
    Called at end of trading to cleanup stuff
    '''
    def cleanup(self):
        return
