from creche.hardware.interfaces.iInhibitableSwitch import IInhibitableSwitch
from creche.hardware.status import Status


class InhibitableSwitch(IInhibitableSwitch):

    def __init__(self, status=Status.OFF, inhibited=False):
        self.__status = status
        self.__inhibited = inhibited

    def on(self):
        new = self
        if not self.__inhibited:
            new = InhibitableSwitch(Status.ON, False)

        return new

    def off(self):
        new = self
        if not self.__inhibited:
            new = InhibitableSwitch(Status.OFF, False)

        return new

    def status(self):
        return self.__status

    def inhibit(self):
        return InhibitableSwitch(self.__status, True)

    def release(self):
        return InhibitableSwitch(self.__status, False)

    def forceOn(self):
        return InhibitableSwitch(Status.ON, True)

    def forceOff(self):
        return InhibitableSwitch(Status.OFF, True)

    def isInhibited(self):
        return self.__inhibited
