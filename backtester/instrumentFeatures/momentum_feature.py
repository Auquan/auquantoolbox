from instrument_feature import InstrumentFeature
import math

class MOMInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        data = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        m = data.sub(data.shift(featureParams['period']), fill_value = 0)[-1]
        return m
