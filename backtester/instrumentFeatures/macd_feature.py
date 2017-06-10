from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma

class MACDInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        avg1 = ma(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period1'])
        avg2 = ma(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period2'])
        return avg1-avg2
