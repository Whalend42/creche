from creche.planning.interfaces.iInstruction import IInstruction
from creche.planning.command import Command

class OffInstruction(IInstruction):

    def __init__(self, index):
        self.__index = index

    def command(self):
        return Command.TURN_OFF

    def index(self):
        return self.__index