from abc import ABCMeta, abstractmethod

class IInstruction(metaclass=ABCMeta):

    @abstractmethod
    def command(self):
        pass
