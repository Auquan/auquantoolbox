from instrument_feature import InstrumentFeature
import math

class MomentumInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        data = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        if len(data.index) > 0:
        	m = data.sub(data.shift(featureParams['period']), fill_value = 0)[-1]
        else:
        	m = 0
        return m
