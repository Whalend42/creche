import asyncio
import websockets
import json

from .const import CMD
from switches.lightshow import LightShow
from switches.switches import Switches

ok_msg = "ok"
success = '1'

separator = '-'

debug_mode = True

el = None
show = None

async def action(websocket, path):
    global el
    global show
    global ok_msg
    global debug_mode

    cmd = None
    
    print("Server started")

    while cmd != CMD["exit"]:

        # get the command
        data = await websocket.recv()
        if debug_mode:
            print("< {}".format(data))
        data = json.loads(data)
        cmd = data["cmd"]
        param = data["param"]

        # run a light show
        if cmd == CMD["run"]:
            if debug_mode:
                print("trying to run lightshow...")
            if show.order is not None:
                show.start()
                if debug_mode:
                    print("lightshow ran normally")
                await websocket.send(ok_msg+"-")
            else:
                if debug_mode:
                    print("warning - Light show not ran beacause no order were defined")
            # todo: else

        # save a program order
        elif cmd == CMD["save"]:
            if debug_mode:
                print("trying to save...")
            if show.order is not None:
                # todo: check cmd[1] is a valid file name
                if param is not None:
                    LightShow.save_order(param, show.order)
                    print("Save complete")
                else:
                    if debug_mode:
                        print("warning - saving failed because no valid name was given")
            else:
                if debug_mode:
                    print("warning - saving failed because no order were defined")
            # todo: both else

        # load an existing program order
        elif cmd == CMD["load"]:
            if debug_mode:
                print("trying to load")
            try:
                order = LightShow.load_order(param)
                show.set_order(order)
                if debug_mode:
                    print("order successfully loaded")
            except FileNotFoundError:
                if debug_mode:
                    print("Failed to load order - File not found")

        # retrieve an order from the received data
        elif cmd == CMD["get"]:
            if debug_mode:
                print("trying to get an order")
            # order = json.loads(cmd[1])
            order = param
            if debug_mode:
                print(order)
            # todo: retrieve the order from the recieved data
            # order = LightShow.order_by_time(order)
            show.set_order(order)
            if debug_mode:
                print("order successfully added")

        # force a switch to the on position
        elif cmd == CMD["on"]:
            if debug_mode:
                print("turning on switch number: "+param)
            show.creche.inhibit_switch(int(param))
            show.creche.force_on(int(param))
            print(show.creche)

        # force a switch to the off position
        elif cmd == CMD["off"]:
            if debug_mode:
                print("turning off switch number: "+param)
            show.creche.inhibit_switch(int(param))
            show.creche.force_off(int(param))
            print(show.creche)

        # quit this method
        elif cmd == CMD["exit"]:
            if debug_mode:
                print("exit server")
            el.stop()
            el.close()

        # invalid command
        else:
            print("invalid command")

        # greeting = "Hello {}!".format(name)
        # await websocket.send(greeting)
        # print("> {}".format(greeting))


def run():
    global el
    global show

    creche = Switches(number_of_switches=16, pin_base=123, devices_ids=0, spi_port=0, console_mode=True)
    order = None
    show = LightShow(order, creche)
    start_server = websockets.serve(action, 'localhost', 8765)
    el = asyncio.get_event_loop()
    el.run_until_complete(start_server)
    el.run_forever()
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
