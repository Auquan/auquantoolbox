class PositionFeature(object):

    @classmethod
    def validateInputs(cls, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureParams, currentFeatures, instrument):
        bookData = instrument.getCurrentBookData()
        instrumentType = instrument.getInstrumentType()
        return instrument.getCurrentPosition()
