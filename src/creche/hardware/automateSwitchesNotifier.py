import time
import threading

from creche.hardware.interfaces.iAutomate import IAutomate

from creche.planning.jsonPlanning import JsonPlanning
#from creche.planning.instruction import Instruction

from creche.planning.command import Command as Cmd

#class AutomateSwitchesNotifier(IAutomate, threading.Thread):
class AutomateSwitchesNotifier(threading.Thread):
    """
    @TODO : 
    - add all methods form iInhibitableSwitches
    """

    def __init__(self, switches, planning, notifiable):
        threading.Thread.__init__(self)
        self.__switches = switches
        self.__planning = planning
        self.__notifiable = notifiable

    def run(self):
        for nextAction in self.__planning.actions():
            if nextAction.command() == Cmd.WAIT:
                self.__notifiable.newStatus(self.__switches.allJsonStatuses())
                time.sleep(nextAction.time())
            elif nextAction.command() == Cmd.TURN_ON:
                self.__switches = self.__switches.on(nextAction.index())
            elif nextAction.command() == Cmd.TURN_OFF:
                self.__switches = self.__switches.off(nextAction.index())

        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

    def on(self, index):
        self.__switches = self.__switches.forceOn(index)
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

    def off(self, index):
        self.__switches = self.__switches.forceOff(index)
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

    def allOff(self):
        self.__switches = self.__switches.forceAllOff()
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

    def allOn(self):
        self.__switches = self.__switches.forceAllOn()
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

