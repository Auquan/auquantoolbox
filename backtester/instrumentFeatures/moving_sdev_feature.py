from instrument_feature import InstrumentFeature


class MovingSDevInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        sdev = instrument.getLookbackFeatures().getData()[featureParams['featureName']][-featureParams['period']:].std()
        return sdev
