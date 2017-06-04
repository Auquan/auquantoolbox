class VwapPriceInstrumentFeature(object):

    @classmethod
    def validateInputs(cls, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, currentFeatures, instrument):
        bookData = instrument.getCurrentBookData()
        instrumentType = instrument.getInstrumentType()
        totalVolume = (bookData['askVolume'] + bookData['bidVolume'])
        if totalVolume > 0:
            vwap = ((bookData['askPrice'] * bookData['askVolume']) + (bookData['bidPrice'] *
                                                                      bookData['bidVolume'])) / totalVolume
            return vwap
        else:
            return 0
