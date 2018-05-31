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

    def emitAllIntrumentUpdates():
        raise NotImplementedError
    '''
    Called at end of trading to cleanup stuff
    '''
    def cleanup(self):
        return
