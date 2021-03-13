class MockedJsonTimeTable():
    
    def __init__(self, file):
        self.__file = file

    def dictonnary(self):
        rawData = {
            "0": [(0, 2), (4, 5)],
            "1": [(1, 3)],
            "2": [(2, 4)],
            "3": [],
            "4": [(3, 5)],
        }
        
        return rawData