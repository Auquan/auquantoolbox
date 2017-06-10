from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma

class MovingAverageInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        data = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        avg = ma(data, featureParams['period'])[-1]
        return avg
        