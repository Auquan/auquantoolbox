from instrument_feature import InstrumentFeature


class MovingAverageInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureParams, currentFeatures, instrument):
        avg = instrument.getLookbackFeatures().getData()[featureParams['featureName']].rolling(window = featureParams['period']).mean()
        return avg
        