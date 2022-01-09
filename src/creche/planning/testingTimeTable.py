class TestingTimeTable():
    
    def __init__(self, size):
        self.__size = size

    def dictonnary(self):
        timing = {}
        for i in range(self.__size):
            timing[i] = [(i+1, i+2)]
        
        return timing