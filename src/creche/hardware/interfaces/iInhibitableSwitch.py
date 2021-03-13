from abc import abstractmethod
from creche.hardware.interfaces.iSwitch import ISwitch

class IInhibitableSwitch(ISwitch):

    @abstractmethod
    def inhibit(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def forceOn(self):
        pass

    @abstractmethod
    def forceOff(self):
        pass

    @abstractmethod
    def isInhibited(self):
        pass

    @abstractmethod
    def jsonStatus(self):
        pass

