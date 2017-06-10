from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma

class MACDInstrumentFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
    	data = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        avg1 = ma(data, featureParams['period1'])
        avg2 = ma(data, featureParams['period2'])
        if len(avg1.index) > 0: 
        	return (avg1 - avg2)[-1]
        else:
        	return 0
