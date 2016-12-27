import time as t
import pickle as p
import threading

import ordering as o
from switches import Switches

class LightShow(threading.Thread):

    def __init__(self, order_by_time, creche):
        threading.Thread.__init__(self)
        # todo: type checking
        self.order_by_time = order_by_time
        self.creche = creche

    def run(self):
        #creche = Switches(number_of_switches=16, pin_base=123, devices_ids=0, spi_port=0, console_mode=True)
        previous_time = 0
        
        for time, switches in sorted(self.order_by_time.items()):
            t.sleep(time - previous_time)
            print("at time: " + str(time) + " activate switches: " + str(switches))
            for switch in switches:
                # change state of switches
                self.creche.inverse_switch(switch)
            print(str(self.creche)+"\n")
            previous_time = time

    def set_order(order):
        # todo: type checking
        self.order = order
    
    @staticmethod
    def order_by_time(order_by_switches):
        order_by_time = {}
        for switch, times in enumerate(order_by_switches):
            for time in times:
                if time in order_by_time:
                    order_by_time[time].append(switch+1)
                else:
                    order_by_time[time] = [switch+1]
        return order_by_time

    @staticmethod
    def save_order(file_name, order):
        with open(file_name, 'wb') as f:
            p.dump(order, f)

    @staticmethod
    def load_order(file_name):
        with open(file_name, 'rb') as f:
            order = p.load(f)
        return order

    #file_name = 'automatic_save.pickle'
    #o.order_by_time = order_by_time(o.order_by_switches)
    #save_order(file_name, o.order_by_time)
    #light_show(load_order(file_name))
    #light_show(o.order_by_time)
