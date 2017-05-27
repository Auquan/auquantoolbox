from datetime import timedelta


class TradingSystemParameters:
    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        return None

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''
    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 5)
