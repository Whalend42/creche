from abc import ABCMeta, abstractmethod

class IAutomate(metaclass=ABCMeta):

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass
