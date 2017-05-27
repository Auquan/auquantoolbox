class LookbackData:
    def __init__(self, size):
        self.__size = size
        self.__storedData = []

    def addData(self, data):
        self.__storedData.append(data)

    def getData(self):
        return self.__storedData
