from abc import abstractmethod
from creche.hardware.interfaces.iSwitches import ISwitches

class IInhibitableSwitches(ISwitches):

    @abstractmethod
    def inhibit(self, i):
        pass

    @abstractmethod
    def release(self, i):
        pass

    @abstractmethod
    def forceOn(self, i):
        pass

    @abstractmethod
    def forceOff(self, i):
        pass

    @abstractmethod
    def inhibitAll(self):
        pass

    @abstractmethod
    def releaseAll(self):
        pass

    @abstractmethod
    def forceAllOn(self):
        pass

    @abstractmethod
    def forceAllOff(self):
        pass

    @abstractmethod
    def isInhibited(self, i):
        pass

    @abstractmethod
    def areInhibited(self):
        pass

