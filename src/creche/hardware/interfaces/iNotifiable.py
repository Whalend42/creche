from abc import ABCMeta, abstractmethod

class INotifiable(metaclass=ABCMeta):

    @abstractmethod
    def newStatus(self, newStatus):
        pass
