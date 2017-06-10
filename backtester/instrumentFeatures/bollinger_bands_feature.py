from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev

class BBandsInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        avg = ma(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period'])
        sdev = msdev(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period'])
        return [avg - sdev, avg + sdev]
