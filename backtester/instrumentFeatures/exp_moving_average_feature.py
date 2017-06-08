from instrument_feature import InstrumentFeature
import math

class ExpMovingAverageInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        if featureKey in instrument.getLookbackFeatures().getData():
            prev_ema = instrument.getLookbackFeatures().getData()[featureKey][-1]
        else:
            prev_ema = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        halflife= featureParams['period']
        alpha =  1 - math.exp(math.log(0.5) / halflife)
        avg = currentFeatures[featureParams['featureName']] * alpha + prev_ema* (1-alpha)
        return avg
