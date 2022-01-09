import sys
import json
import time
import asyncio

sys.path.append("src/")

from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.inhibitableSwitches import InhibitableSwitches
from creche.hardware.status import Status
from creche.planning.jsonPlanning import JsonPlanning
from creche.planning.testingTimeTable import TestingTimeTable
from creche.server.websocketServer import WebsocketServer


if __name__ == "__main__":
    size = 5
    switches = InhibitableSwitches([InhibitableSwitch(status=Status.OFF, inhibited=False)]*size)
    testPlanning = JsonPlanning(TestingTimeTable(size))
    websocketServer = WebsocketServer(switches, testPlanning)
    asyncio.run(websocketServer.run())
    
