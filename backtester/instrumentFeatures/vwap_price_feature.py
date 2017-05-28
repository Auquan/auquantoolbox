from instrument_feature import InstrumentFeature


class VwapPriceInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, currentFeatures, instrument):
        bookData = instrument.getCurrentBookData()
        instrumentType = instrument.getInstrumentType()
        vwap = ((bookData['askPrice']*bookData['askVolume'])+(bookData['bidPrice']*bookData['bidVolume']))/(bookData['askVolume']+bookData['bidVolume'])
        return 'price', vwap
