from feature import Feature
from backtester.financial_fn import ma


class MARibbonFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        rolling_means = np.zeros(featureParams['numRibbons'])
        if len(data) < 1:
        	return rolling_means
        for i in np.linspace(featureParams['startPeriod'], 
        							featureParams['endPeriod'], 
        							int((featureParams['endPeriod'] - featureParams['startPeriod'])/featureParams['numRibbons'])):
    		rolling_means[i] = data[-i:].mean()
        
        return rolling_means
