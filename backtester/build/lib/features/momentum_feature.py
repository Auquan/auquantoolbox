from feature import Feature


class MomentumFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) > featureParams['period']:
            m = data[-1]/data[-featureParams['period']] * 100
        else:
            m = 0
        return m
