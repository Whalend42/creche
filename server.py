import asyncio
import websockets

from lightshow import LightShow
from switches import Switches





# actions: 
# 0  quit
# 1  run lightshow
# 2  save program as X
# 3  load program X
# 4  get order
# 5  turn on switch number X
# 6  turn off switch number X


actions = []
actions["exit"] = 0
actions["run"] = 1
actions["save"] = 2
actions["load"] = 3
actions["get"] = 4
actions["on"] = 5
actions["off"] = 6

async def action(websocket, path):
    global el
    global actions
    global show

    cmd = await websocket.recv()
    print("< {}".format(cmd))

    cmd = cmd.split('-')

    if cmd[0] == actions["run"]:
        if show.order is not None:
            show.start()
        #todo: else
    elif cmd[0] == actions["save"]:
        if show.order is not None:
            #todo: check cmd[1] is a valid file name
            if cmd[1] is not None:
                LightShow.save_order(cmd[1], show.order)
        #todo: both else
    elif cmd[0] == actions["load"]:
        LightShow.load_order(cmd[1])
    elif cmd[0] == actions["get"]:
        # retrieve the order from the recieved data
        order = LightShow.order_by_time(order)
        show.set_order(order)
    elif cmd[0] == actions["on"]:
        show.creche.inhibit_switch(cmd[1])
        show.creche.force_on(cmd[1])
    elif cmd[0] == actions["off"]:
        show.creche.inhibit_switch(cmd[1])
        show.creche.force_off(cmd[1])
    elif cmd[0] == actions["exit"]:
        el.stop()
        #el.close()



    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))




creche = Switches(number_of_switches=16, pin_base=123, devices_ids=0, spi_port=0, console_mode=True)
order = None
show = LightShow(creche, order)
start_server = websockets.serve(action, 'localhost', 8765)
el = asyncio.get_event_loop()
el.run_until_complete(start_server)
el.run_forever()
#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()
