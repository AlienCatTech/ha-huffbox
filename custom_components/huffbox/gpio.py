import os

import gpiod
from gpiod.line import Direction, Value

from .const import NAME


class HuffBoxGPIO:
    def __init__(self) -> None:
        self.lines = None
        self.pin_map = {"lock": 26, "fan": 19, "light": 13}
        self._state = {"lock": False, "fan": False, "light": True}
        self.reverse_map = {"lock": False, "fan": False, "light": True}
        self.chip_name = "/dev/gpiochip4"
        self.init_gpio_line()

    def is_gpio(self):
        return os.path.exists(self.chip_name)

    def init_gpio_line(self):
        if self.is_gpio():
            config = {
                self.pin_map[x]: gpiod.LineSettings(direction=Direction.OUTPUT)
                for x in self.pin_map
            }

            self.lines = gpiod.request_lines(
                self.chip_name,
                consumer=NAME,
                config=config,
            )

    def get_gpio_state(self, device) -> bool:
        """Get GPIO pin state."""
        return self._state[device]

    def set_gpio_state(self, device: str, state: bool):
        pin = self.pin_map[device]
        reverse = self.reverse_map[device]
        value = Value.ACTIVE if state else Value.INACTIVE
        if reverse:
            value = Value.INACTIVE if value == Value.ACTIVE else Value.ACTIVE
        if self.is_gpio() and self.lines:
            self.lines.set_value(pin, value)
        self._state[device] = state

    def get_gpio_pin(self, device):
        """Get GPIO pin state."""
        return str(self.pin_map[device])

    def set_gpio_pin(self, device: str, pin: int):
        self.pin_map[device] = pin
        self.close()
        self.init_gpio_line()

    def close(self):
        if self.is_gpio() and self.lines:
            self.lines.release()
