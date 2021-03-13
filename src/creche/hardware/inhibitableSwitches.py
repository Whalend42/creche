import copy
import json

from creche.hardware.interfaces.iInhibitableSwitch import IInhibitableSwitch
from creche.hardware.interfaces.iInhibitableSwitches import IInhibitableSwitches
from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.status import Status


class InhibitableSwitches(IInhibitableSwitches):

    def __init__(self, switches):
        self.__switches = switches

    def isValidPosition(self, i):
        return 0 <= i < len(self.__switches)

    def on(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        if not self.__switches[i].isInhibited():
            new[i] = InhibitableSwitch(Status.ON, False)

        return InhibitableSwitches(new)

    def off(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        if not self.__switches[i].isInhibited():
            new[i] = InhibitableSwitch(Status.OFF, False)

        return InhibitableSwitches(new)

    def status(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        return self.__switches[i].status()

    def allOn(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            if not self.__switches[i].isInhibited():
                new[i] = InhibitableSwitch(Status.ON, False)

        return InhibitableSwitches(new)

    def allOff(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            if not self.__switches[i].isInhibited():
                new[i] = InhibitableSwitch(Status.OFF, False)

        return InhibitableSwitches(new)

    def allStatuses(self):
        statuses = []
        for switch in self.__switches:
            statuses.append(switch.status())

        return statuses

    def inhibit(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        new[i] = InhibitableSwitch(self.__switches[i].status(), True)
        return InhibitableSwitches(new)

    def release(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        new[i] = InhibitableSwitch(self.__switches[i].status(), False)
        return InhibitableSwitches(new)

    def forceOn(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        new[i] = InhibitableSwitch(Status.ON, True)

        return InhibitableSwitches(new)

    def forceOff(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.__switches)
        new[i] = InhibitableSwitch(Status.OFF, True)

        return InhibitableSwitches(new)

    def inhibitAll(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            new[i] = InhibitableSwitch(self.status(i), True)

        return InhibitableSwitches(new)

    def releaseAll(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            new[i] = InhibitableSwitch(self.status(i), False)

        return InhibitableSwitches(new)

    def forceAllOn(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            new[i] = InhibitableSwitch(Status.ON, True)

        return InhibitableSwitches(new)

    def forceAllOff(self):
        new = copy.deepcopy(self.__switches)
        for i in range(len(self.__switches)):
            new[i] = InhibitableSwitch(Status.OFF, True)

        return InhibitableSwitches(new)

    def isInhibited(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        return self.__switches[i].isInhibited()

    def areInhibited(self):
        statuses = []
        for switch in self.__switches:
            statuses.append(switch.isInhibited())

        return statuses

    def jsonStatus(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        return self.__switches[i].jsonStatus()

    def allJsonStatuses(self):
        fullStatuses = []
        index = 0
        for switch in self.__switches:
            obj = {
                "status": json.loads(switch.jsonStatus()),
                "index": index,
            }
            fullStatuses.append(obj)
            index += 1

        return json.dumps(fullStatuses)
