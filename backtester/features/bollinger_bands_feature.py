from feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        sdev = data[-featureParams['period']:].std()
        if len(data) < 1:
        	return [0,0]
        return [(avg - sdev), (avg + sdev)]
            
