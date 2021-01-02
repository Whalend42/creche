import copy
from creche.hardware.interfaces.iInhibitableSwitch import IInhibitableSwitch
from creche.hardware.interfaces.iInhibitableSwitches import IInhibitableSwitches
from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.status import Status


class InhibitableSwitches(IInhibitableSwitches):

    def __init__(self, switches):
        self.switches = switches

    def isValidPosition(self, i):
        return 0 <= i < len(self.switches)

    def on(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        if not self.switches[i].isInhibited():
            new[i] = InhibitableSwitch(Status.ON, False)

        return InhibitableSwitches(new)

    def off(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        if not self.switches[i].isInhibited():
            new[i] = InhibitableSwitch(Status.OFF, False)

        return InhibitableSwitches(new)

    def status(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        return self.switches[i].status()

    def allOn(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            if not self.switches[i].isInhibited():
                new[i] = InhibitableSwitch(Status.ON, False)

        return InhibitableSwitches(new)

    def allOff(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            if not self.switches[i].isInhibited():
                new[i] = InhibitableSwitch(Status.OFF, False)

        return InhibitableSwitches(new)

    def allStatuses(self):
        statuses = []
        for switch in self.switches:
            statuses.append(switch.status())

        return statuses

    def inhibit(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        new[i] = InhibitableSwitch(self.switches[i].status(), True)
        return InhibitableSwitches(new)

    def release(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        new[i] = InhibitableSwitch(self.switches[i].status(), False)
        return InhibitableSwitches(new)

    def forceOn(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        new[i] = InhibitableSwitch(Status.ON, True)

        return InhibitableSwitches(new)

    def forceOff(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        new = copy.deepcopy(self.switches)
        new[i] = InhibitableSwitch(Status.OFF, True)

        return InhibitableSwitches(new)

    def inhibitAll(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            new[i] = InhibitableSwitch(self.status(i), True)

        return InhibitableSwitches(new)

    def releaseAll(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            new[i] = InhibitableSwitch(self.status(i), False)

        return InhibitableSwitches(new)

    def forceAllOn(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            new[i] = InhibitableSwitch(Status.ON, True)

        return InhibitableSwitches(new)

    def forceAllOff(self):
        new = copy.deepcopy(self.switches)
        for i in range(len(self.switches)):
            new[i] = InhibitableSwitch(Status.OFF, True)

        return InhibitableSwitches(new)

    def isInhibited(self, i):
        if not self.isValidPosition(i):
            raise Exception("Invalid position")

        return self.switches[i].isInhibited()

    def areInhibited(self):
        statuses = []
        for switch in self.switches:
            statuses.append(switch.isInhibited())

        return statuses
