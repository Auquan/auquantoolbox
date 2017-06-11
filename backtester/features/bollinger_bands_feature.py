from feature import Feature
from backtester.financial_fn import ma
from backtester.financial_fn import msdev


class BollingerBandsFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        avg = ma(lookbackDataDf[featureParams['featureName']], featureParams['period'])
        sdev = msdev(lookbackDataDf[featureParams['featureName']], featureParams['period'])
        if len(avg.index) > 0:
            return [(avg - sdev)[-1], (avg + sdev)[-1]]
        else:
            return [avg, avg]
