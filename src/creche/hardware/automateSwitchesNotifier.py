import time
import threading

from creche.hardware.interfaces.iAutomate import IAutomate
from creche.planning.jsonPlanning import JsonPlanning
from creche.planning.command import Command as Cmd

class AutomateSwitchesNotifier(IAutomate, threading.Thread):

    def __init__(self, switches, planning, notifiable):
        threading.Thread.__init__(self)
        self.__switches = switches
        self.__planning = planning
        self.__notifiable = notifiable
        self.__stop = False
        self.__lockAction = threading.Lock()
        self.__lockPause = threading.Lock()
        self.__lockPlay = threading.Lock()
        self.__lockPlay.acquire()
        self.__terminate = False

    def __runAutomate(self):
        self.__initThread()
        for nextAction in self.__planning.actions():
            self.__lockPause.acquire()

            if self.__stop:
                self.__stopThread()
                break
                
            if nextAction.command() == Cmd.WAIT:
                self.__notifiable.newStatus(self.__switches.allJsonStatuses())
                time.sleep(nextAction.time())
            elif nextAction.command() == Cmd.TURN_ON:
                self.__switches = self.__switches.on(nextAction.index())
            elif nextAction.command() == Cmd.TURN_OFF:
                self.__switches = self.__switches.off(nextAction.index())

            if self.__lockPause.locked():
                self.__lockPause.release()

            # just to give time before next lockPause acquire 
            # for a pause action to do acquire
            time.sleep(0.01)

        self.__notifiable.newStatus(self.__switches.allJsonStatuses())

    def run(self):
        while not self.__terminate:
            self.__lockPlay.acquire()
            if self.__terminate:
                break
            self.__runAutomate()

    def __releaseAllLocks():
        if self.__lockPause.locked():
            self.__lockPause.release()
        if self.__lockPlay.locked():
            self.__lockPlay.release()
        if self.__lockAction.locked():
            self.__lockAction.release()

    def terminate(self):
        self.__lockAction.acquire()
        self.__terminate = True
        if self.__lockPlay.locked():
            self.__lockPlay.release()
        self.__lockAction.release()

    def play(self):
        self.__lockAction.acquire()
        if self.__lockPlay.locked():
            self.__lockPlay.release()
        self.__lockAction.release()

    def __initThread(self):
        self.__stop = False
        self.__switches = self.__switches.allOff()
        if self.__lockPause.locked():
            self.__lockPause.release()

    def stop(self):
        self.__lockAction.acquire()
        self.__stop = True
        if self.__lockPause.locked():
            self.__lockPause.release()

    def __stopThread(self):
        self.__switches = self.__switches.releaseAll()
        self.__switches = self.__switches.allOff()
        self.__lockAction.release()

    def pause(self):
        self.__lockAction.acquire()
        self.__lockPause.acquire()
        self.__lockAction.release()

    def resume(self):
        self.__lockAction.acquire()
        if self.__lockPause.locked():
            self.__lockPause.release()
        self.__lockAction.release()

    def loadPlanning(self, planning):
        self.__lockAction.acquire()
        self.__planning = planning
        self.__lockAction.release()

    def on(self, index):
        self.__lockAction.acquire()
        self.__switches = self.__switches.forceOn(index)
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())
        self.__lockAction.release()

    def off(self, index):
        self.__lockAction.acquire()
        self.__switches = self.__switches.forceOff(index)
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())
        self.__lockAction.release()

    def allOff(self):
        self.__lockAction.acquire()
        self.__switches = self.__switches.forceAllOff()
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())
        self.__lockAction.release()

    def allOn(self):
        self.__lockAction.acquire()
        self.__switches = self.__switches.forceAllOn()
        self.__notifiable.newStatus(self.__switches.allJsonStatuses())
        self.__lockAction.release()

