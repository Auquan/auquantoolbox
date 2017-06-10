from instrument_feature import InstrumentFeature
import math
from backtester.financial_fn import ema

class ExpMovingAverageInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        data = instrument.getLookbackFeatures().getData()[featureKey]
        if len(data.index) > 0:
            prev_ema = data[-1]
        else:
            prev_ema = currentFeatures[featureParams['featureName']]
        halflife= featureParams['period']
        alpha =  1 - math.exp(math.log(0.5) / halflife)
        avg = currentFeatures[featureParams['featureName']] * alpha + prev_ema* (1-alpha)
        return avg
