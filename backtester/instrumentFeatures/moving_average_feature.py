from instrument_feature import InstrumentFeature


class MovingAverageInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        avg = instrument.getLookbackFeatures().getData()[featureParams['featureName']][-featureParams['period']:].mean()
        return avg
        