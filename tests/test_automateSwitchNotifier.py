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
from creche.planning.mockedJsonTimeTable import MockedJsonTimeTable, MockedJsonTimeTable2
from creche.hardware.interfaces.iNotifiable import INotifiable


class FakeServer(INotifiable):

    def __init__(self, switches, planning):
        self.__startTime = 0
        self.__automate = AutomateSwitchesNotifier(switches, planning, self)
        self.__automate.start()

    def start(self):
        self.__startTime = datetime.now()
        self.__automate.play()

    def stop(self):
        print("STOOOOP!!!!!!")
        #self.__automate.allOff()
        self.__automate.stop()

    def pause(self):
        # print("PAUSE!!!!!!")
        self.__automate.pause()

    def resume(self):
        # print("RESUME!!!!!!")
        self.__automate.resume()

    def automate(self):
        return self.__automate

    def terminate(self):
        print("Final end!!!!!!")
        self.__automate.terminate()

    def loadPlanning(self, planning):
        print("New planning!!!!!!")
        self.__automate.loadPlanning(planning)

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
time.sleep(2.1)
# print("pause for 4 seconds!")
# server.pause()
# time.sleep(4)
# server.resume()
# print("resume")

# time.sleep(2.1)
server.stop()
time.sleep(5)
# time.sleep(3.1)
# print("Restart!")
print("Second program")
server.loadPlanning(JsonPlanning(MockedJsonTimeTable2(filename)))
server.start()
time.sleep(10)
server.stop()
server.terminate()
print("The end")

