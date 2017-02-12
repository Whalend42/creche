from .const import ON, OFF


class Switches:
    """
    The wrapper class containing every information about the switches
    """

    class __Singleton:
        """
        The inside class.
        """

        def __init__(self, number_of_switches, pin_base=123, devices_ids=0, spi_port=0, console_mode=True):
            """
            For initalization of all witches connected through an "mcp23s17"
            Initialize switches [0, 'number_of_switches'[ to output mode

            """
            self._console_mode = console_mode
            self._number_of_switches = number_of_switches
            range_pins = range(pin_base, pin_base+number_of_switches)
            
            if not console_mode:
                self._pin_base = pin_base

                wp.wiringPiSetup()

                if isinstance(devices_ids, list):
                    for dev_id in devices_ids:
                        wp.mcp23s17Setup(pin_base, spi_port, dev_id)
                else:
                    wp.mcp23s17Setup(pin_base, spi_port, devices_ids)

            # set all switches to output mode and create an array containg the state of all of them
            output_mode = 1
            self._state = []
            self._inhibited = []
            for i in range_pins:
                if not console_mode:
                    wp.pinMode(i, output_mode)
                self._state.append(OFF)
                self._inhibited.append(False)

        def inhibit_switch(self, switch_number):
            self._inhibited[switch_number-1] = True

        def inhibit_all(self):
            self._inhibited = [True]*self._number_of_switches

        def cancel_inhibit_switch(self, switch_number):
            self._inhibited[switch_number-1] = False

        def cancel_inhibit_all(self):
            self._inhibited = [False]*self._number_of_switches

        def force_on(self, switch_number):
            self._state[switch_number-1] = ON
            if not self._console_mode:
                wp.digitalWrite(switch_number-1, ON)

        def force_off(self, switch_number):
            self._state[switch_number-1] = OFF
            if not self._console_mode:
                wp.digitalWrite(switch_number-1, OFF)

        def inverse_switch(self, switch_number):
            if not self._inhibited[switch_number-1]:
                self._state[switch_number-1] ^= 1
                if not self._console_mode:
                    wp.digitalWrite(switch_number-1, self._state[switch_number-1])

        def reset_all(self):
            for i in range(0, self._number_of_switches):
                if not self._inhibited[i]:
                    self._state[i] = OFF

        def __str__(self):
            str_repr = ''
            for i in range(0, self._number_of_switches):
                if self._state[i] == 1:
                    str_repr += "| ** "
                else:
                    str_repr += "| -- "
            str_repr += "|\n"
            for i in range(1, self._number_of_switches+1):
                str_repr += '| {0:2d} '.format(i)

            return str_repr+"|"

    # the property containing the only instance of the actual class
    instance = None

    def __init__(self, number_of_switches, pin_base=123, devices_ids=0, spi_port=0, console_mode=True):
        """

        :param number_of_switches:
        :param pin_base:
        :param devices_ids:
        :param spi_port:
        :param console_mode:
        """

        if not console_mode:
            import wiringpi as wp

        if Switches.instance is None:
            Switches.instance = Switches.__Singleton(number_of_switches, pin_base, devices_ids, spi_port, console_mode)
        else:
            Switches.instance.number_of_switches = number_of_switches
            Switches.instance.pin_base           = pin_base
            Switches.instance.devices_ids        = devices_ids
            Switches.instance.spi_port           = spi_port
            Switches.instance.console_mode       = console_mode

    def __str__(self):
        return str(Switches.instance)

    def __getattr__(self, name):
        return getattr(self.instance, name)
