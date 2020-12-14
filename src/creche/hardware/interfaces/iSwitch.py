from abc import ABCMeta, abstractmethod

class ISwitch(metaclass=ABCMeta):

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass
 
    @abstractmethod
    def status(self):
        pass

