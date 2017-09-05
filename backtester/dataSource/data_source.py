class DataSource(object):
    # emits list of instrument updates at the same time.
    # The caller needs to ensure all these updates are happening at the same time
    # emits [t1, [i1, i2, i3]], where i1, i2, i3 are updates happening at time t1
    def emitInstrumentUpdates(self):
        raise NotImplementedError
