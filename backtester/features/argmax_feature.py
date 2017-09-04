from feature import Feature


class ArgMaxFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        # avg = ma(data, featureParams['period'])
        if len(data) < 1:
            return 0
        return data[-featureParams['period']:].idxmax()
