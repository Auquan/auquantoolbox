from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureParams, featureKey, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureParams, featureKey, currentFeatures, instrument):
        avg = ma(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period'])
        sdev = msdev(instrument.getLookbackFeatures().getData()[featureParams['featureName']], featureParams['period'])
        if len(avg.index) > 0:
            return [(avg - sdev)[-1], (avg + sdev)[-1]]
        else:
            return [avg, avg]
