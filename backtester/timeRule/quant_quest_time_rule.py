from backtester.timeRule.time_rule import TimeRule
from datetime import datetime, timedelta
import os
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class QuantQuestTimeRule(TimeRule):
    def __init__(self, cachedFolderName, dataSetId):
        self.__cachedFolderName = cachedFolderName
        self.__dataSetId = dataSetId
        self.ensureDirectoryExists(cachedFolderName, dataSetId)

    def ensureDirectoryExists(self, cachedFolderName, dataSetId):
        if not os.path.exists(cachedFolderName):
            os.mkdir(cachedFolderName, 0o755)
        if not os.path.exists(cachedFolderName + '/' + dataSetId):
            os.mkdir(cachedFolderName + '/' + dataSetId)

    def getFileName(self):
        return self.__cachedFolderName + self.__dataSetId + '/date_list.txt'

    def downloadFile(self, dataSetId, downloadLocation):
        url = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/date_list.txt' % (
            dataSetId)
        response = urlopen(url)
        status = response.getcode()
        if status == 200:
            print('Downloading date list to file: %s' % (downloadLocation))
            with open(downloadLocation, 'w') as f:
                f.write(response.read().decode('utf8'))
            return True
        else:
            logError('File not found. Please check settings!')
            return False

    def emitTimeToTrade(self):
        fileName = self.getFileName()
        if not os.path.exists(self.__cachedFolderName):
            os.mkdir(self.cachedFolderName, 0o755)
        if not os.path.isfile(fileName):
            if not self.downloadFile(self.__dataSetId, fileName):
                logError('File not found %s:' % (fileName))
                return

        with open(fileName) as f:
            for line in f:
                dateStr = line.rstrip()
                dateOfUpdate = datetime.strptime(dateStr, '%Y-%m-%d')
                start = dateOfUpdate + timedelta(minutes=17, hours=9)
                end = dateOfUpdate + timedelta(minutes=29, hours=15)
                current = start
                while (current <= end):
                    yield current
                    current += timedelta(minutes=1)
