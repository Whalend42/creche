from creche.planning.interfaces.iInstruction import IInstruction
from creche.planning.command import Command

class WaitInstruction(IInstruction):

    def __init__(self, time):
        self.__time = time

    def command(self):
        return Command.WAIT

    def time(self):
        return self.__time