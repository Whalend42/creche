from abc import ABCMeta, abstractmethod

class IAutomate(metaclass=ABCMeta):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
