from abc import ABCMeta, abstractmethod

class ISwitches(metaclass=ABCMeta):

    @abstractmethod
    def on(self, i):
        pass

    @abstractmethod
    def off(self, i):
        pass
 
    @abstractmethod
    def status(self, i):
        pass

    @abstractmethod
    def allOn(self):
        pass

    @abstractmethod
    def allOff(self):
        pass

    @abstractmethod
    def allStatuses(self):
        pass

