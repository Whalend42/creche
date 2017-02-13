import asyncio
import websockets
import json

async def some_tests():
    async with websockets.connect('ws://localhost:8765') as websocket:
        
        cmd = None

        while cmd != '0':
            print("enter a cmd:")
            print("0 to exit")
            print("1 to run")
            print("2-filename to save")
            print("3-filename to load")
            print('4-{"time1":[x,y]} to get')
            print("5-x to force on")
            print("6-x to force off")
            cmd = input("cmd  > ")
            if cmd == "4":
                param = input("param> ")
                param = json.loads(param)
            else:
                param = input("param> ")

            await websocket.send(json.dumps({'cmd': cmd, 'param': param}))

try:
    asyncio.get_event_loop().run_until_complete(some_tests())
except OSError:
    print("Server is not online")
