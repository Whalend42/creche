import asyncio
import websockets

import lightshow as li
from switches import Switches





# actions: 
# 1  run lightshow
# 2  save program as X
# 3  load program X
# 4  turn on switch number X
# 5  turn off switch number X
# 6  quit

actions = []
actions["run"] = 1
actions["save"] = 2
actiosn["load"] = 3
actions["on"] = 4
actions["off"] = 5
actions["exit"] = 6

async def action(websocket, path):
    global creche
    global el
    global actions
    global order

    cmd = await websocket.recv()
    print("< {}".format(cmd))

    cmd = cmd.split('-')

    if cmd[0] == actions["run"]:
        if order is not None:
            li.lightshow(order, creche)
        #todo: else
    elif cmd[0] == actions["save"]:
        if order is not None:
            #todo: check cmd[1] is a valid file name
            if cmd[1] is not None:
                li.save_order(cmd[1],order)
        #todo: both else
    elif cmd[0] == actions["load"]:

    elif cmd[0] == actions["on"]:
    elif cmd[0] == actions["off"]:
    elif cmd[0] == actions["exit"]:
        el.stop()
        el.close()



    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))





creche = Switches(number_of_switches=16, pin_base=123, devices_ids=0, spi_port=0, console_mode=True)
order = None
start_server = websockets.serve(action, 'localhost', 8765)
el = asyncio.get_event_loop()
el.run_until_complete(start_server)
el.run_forever()
#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()
