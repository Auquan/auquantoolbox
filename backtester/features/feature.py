class Feature:
    def __init__(self, identifier):
        self.identifier = identifier

    def convertToString(self):
        raise NotImplementedError
