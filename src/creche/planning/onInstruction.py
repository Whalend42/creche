from creche.planning.interfaces.iInstruction import IInstruction
from creche.planning.command import Command

class OnInstruction(IInstruction):

    def __init__(self, index):
        self.__index = index

    def command(self):
        return Command.TURN_ON

    def index(self):
        return self.__index