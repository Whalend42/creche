import asyncio
import websockets
import json
from datetime import datetime

from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.inhibitableSwitches import InhibitableSwitches
from creche.planning.jsonPlanning import JsonPlanning
from creche.planning.testingTimeTable import TestingTimeTable
from creche.hardware.interfaces.iNotifiable import INotifiable
from creche.hardware.automateSwitchesNotifier import AutomateSwitchesNotifier


class WebsocketServer(INotifiable):

    def __init__(self, switches, planning):
        self.__connections = []
        self.__startTime = 0
        self.__automate = AutomateSwitchesNotifier(switches, planning, self)
        self.__automate.start()

    async def handler(self, websocket):
        self.__connections.append(websocket)
        while True:
            msg = ""
            try:
                msg = await websocket.recv()
            except websockets.ConnectionClosedOK:
                print("Client disconnected")
                break
            print(f"INCOMING < {str(msg)}")
            resp = await self.executeAction(msg)


    async def run(self):
        async with websockets.serve(self.handler, "localhost", 9999):
            await asyncio.Future()


    async def newStatus(self, newStatus):
        self.printJson(newStatus)
        for websocket in self.__connections:
            await websocket.send(newStatus)


    async def executeAction(self, jsonInstruction):
        print(f"execute action: {jsonInstruction}")
        instruction = json.loads(jsonInstruction)
        command = instruction["action"]
        if command == 'play':
            self.__startTime = datetime.now()
            self.__automate.play()
        elif command == 'stop':
            self.__automate.stop()
        elif command == 'pause':
            self.__automate.pause()
        elif command == 'resume':
            self.__automate.resume()
        elif command == 'terminate':
            self.__automate.terminate()
        elif command == 'loadPlanning':
            self.__automate.loadPlanning(instruction["planning"])
        elif command == 'status':
            await self.__automate.sendStatuses()
        else:
            print("invalid instruction")
        return 1


    def printJson(self, jsonStatuses):
        elapsedTime = 0
        if (self.__startTime != 0):
            elapsedTime = datetime.now() - self.__startTime
        print("After "+str(elapsedTime)+", status: ")
        dic = json.loads(jsonStatuses)
        for sw in dic:
            status = "On" if sw["status"]["isOn"] else "Off"
            blocked = "blocked" if sw["status"]["isInhibited"] else "free"
            print(status+"("+blocked+") - "+str(sw["index"]))
        print("**********************")


if __name__ == "__main__":
    size = 5
    switches = InhibitableSwitches([InhibitableSwitch(status=Status.OFF, inhibited=False)]*size)
    testPlanning = JsonPlanning(TestingTimeTable(size))
    websocketServer = WebsocketServer(switches, testPlanning)
    asyncio.run(websocketServer.run())