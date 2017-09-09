from backtester.features.feature import Feature

class ProfitabilityFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
    	pnlKey = 'pnl'
    	countKey = 'count'
    	if 'pnlKey' in featureParams:
    		pnlKey = featureParams['pnlKey']
    	if 'countKey' in featureParams:
    		countKey = featureParams['countKey']

        prevData = lookbackDataDf[featureKey].iloc[-1]
        prevCount = lookbackDataDf[countKey].iloc[-1]
        accurateCount = prevCount*prevData
        if (lookbackDataDf[pnlKey].iloc[-1] > 0):
        	accurateCount += 1
        prevCount+=1
        return float(accurateCount)/float(prevCount)

