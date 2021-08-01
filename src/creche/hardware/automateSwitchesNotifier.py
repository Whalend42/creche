import time
import threading

from creche.hardware.interfaces.iAutomate import IAutomate

from creche.planning.jsonPlanning import JsonPlanning
#from creche.planning.instruction import Instruction

from creche.planning.command import Command as Cmd

class AutomateSwitchesNotifier(IAutomate, threading.Thread):
#class AutomateSwitchesNotifier(threading.Thread):

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
                print("[Thread] Automate - stop current")
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
            # for an pause action to do acquire
            time.sleep(0.01)

        self.__notifiable.newStatus(self.__switches.allJsonStatuses())
        print("[Thread] Automate - THE END")

    def run(self):
        while not self.__terminate:
            self.__lockPlay.acquire()
            if self.__terminate:
                break
            self.__runAutomate()
        print("[Thread] Automate - THE END FOREVER")

    def __releaseAllLocks():
        # release all locks
        if self.__lockPause.locked():
            self.__lockPause.release()
        if self.__lockPlay.locked():
            self.__lockPlay.release()
        if self.__lockAction.locked():
            self.__lockAction.release()

    def terminate(self):
        self.__lockAction.acquire()
        print("Terminate action starting")
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
        print("stop action part 1 1")
        self.__lockAction.acquire()
        print("stop action part 1 2")
        self.__stop = True
        print("stop action part 1 3")
        if self.__lockPause.locked():
            print("stop action part 1 release pause")
            self.__lockPause.release()
        print("stop action part 1 4")

    def __stopThread(self):
        print("stop action part 2")
        self.__switches = self.__switches.releaseAll()
        self.__switches = self.__switches.allOff()
        self.__lockAction.release()
        print("stop action finished")

    def pause(self):
        self.__lockAction.acquire()
        self.__lockPause.acquire()
        print("Sould be paused")
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

