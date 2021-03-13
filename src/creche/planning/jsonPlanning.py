import collections

from creche.planning.onInstruction import OnInstruction
from creche.planning.offInstruction import OffInstruction
from creche.planning.waitInstruction import WaitInstruction
from creche.planning.command import Command as Cmd
#from creche.planning.FileStoredJsonPlanning import FileStoredJsonPlanning

class JsonPlanning():

    def __init__(self, jsonTimeTable):
        self.__jsonTimeTable = jsonTimeTable

    def generateInstructions(self, rawData):
        unorderedActions = {}
        for index, timings in rawData.items():
            for timing in timings:
                timeOn = timing[0]
                timeOff = timing[1]

                on = OnInstruction(int(index))
                off = OffInstruction(int(index))

                if unorderedActions.get(timeOn) == None:
                    unorderedActions[timeOn] = [on]
                else:
                    unorderedActions[timeOn].append(on)

                if unorderedActions.get(timeOff) == None:
                    unorderedActions[timeOff] = [off]
                else:
                    unorderedActions[timeOff].append(off)

        return collections.OrderedDict(sorted(unorderedActions.items()))

    def actions(self):
        rawData = self.__jsonTimeTable.dictonnary()
        timedInstructions = self.generateInstructions(rawData)

        previousTime = 0
        for time, instructions in timedInstructions.items():
            yield WaitInstruction(time - previousTime)
            previousTime = time

            for instruction in instructions:
                yield instruction


                


