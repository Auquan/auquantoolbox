from instrument_feature import InstrumentFeature
from backtester.financial_fn import ma


class RSIFeature(InstrumentFeature):

    @classmethod
    def validateInputs(cls, featureKey, featureParams, currentFeatures, instrument):
        return True

    @classmethod
    def compute(cls, featureKey, featureParams, currentFeatures, instrument):
        data = instrument.getLookbackFeatures().getData()[featureParams['featureName']]
        data_upside=data.sub(data.shift(1), fill_value = 0)
    	data_downside = data_upside.copy()
    	data_downside[data_upside>0] = 0
    	data_upside[data_upside<0] = 0
    	avg_upside = ma(data_upside, featureParams['period'])[-1]
    	avg_downside = ma(data_downside, featureParams['period'])[-1]
    	rs = -avg_upside/avg_downside
    	return 100-(100/(1+rs))
        