from feature import Feature


class MomentumFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) > 0:
            m = data.sub(data.shift(featureParams['period']), fill_value=0)[-1]
        else:
            m = 0
        return m
