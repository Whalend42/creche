import sys
from datetime import datetime
import json

sys.path.append("../src/")

import time

from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.inhibitableSwitches import InhibitableSwitches
from creche.hardware.status import Status
from creche.hardware.automateSwitchesNotifier import AutomateSwitchesNotifier
from creche.planning.jsonPlanning import JsonPlanning
from creche.planning.mockedJsonTimeTable import MockedJsonTimeTable
from creche.hardware.interfaces.iNotifiable import INotifiable


class FakeServer(INotifiable):

    def __init__(self, switches, planning):
        self.__startTime = 0
        self.__automate = AutomateSwitchesNotifier(switches, planning, self)

    def start(self):
        self.__startTime = datetime.now()
        self.__automate.start()

    def offAll(self):
        print("STOOOOP!!!!!!")
        self.__automate.allOff()


    def newStatus(self, newStatus):
        elapsedTime = datetime.now() - self.__startTime
        print("After "+str(elapsedTime)+", status: ")
        self.printJson(newStatus)
        #self.printJson(self.__switches.allJsonStatuses())

    def printJson(self, jsonStatuses):
        dic = json.loads(jsonStatuses)
        for sw in dic:
            status = "On" if sw["status"]["isOn"] else "Off"
            blocked = "blocked" if sw["status"]["isInhibited"] else "free"
            print(status+"("+blocked+") - "+str(sw["index"]))
        print("**********************")

    
size = 5
filename = "file.name"
switches = InhibitableSwitches([InhibitableSwitch(status=Status.OFF, inhibited=False)]*size)
planning = JsonPlanning(MockedJsonTimeTable(filename))

server = FakeServer(switches, planning)
server.start()

time.sleep(4.1)
server.offAll()
time.sleep(10)


