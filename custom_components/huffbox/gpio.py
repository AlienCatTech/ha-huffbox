from pathlib import Path

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

    def is_gpio(self) -> bool:
        return Path(self.chip_name).exists()

    def init_gpio_line(self) -> None:
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

    def get_gpio_state(self, device: str) -> bool:
        """Get GPIO pin state."""
        return self._state[device]

    def set_gpio_state(self, device: str, state: bool) -> None:
        pin = self.pin_map[device]
        reverse = self.reverse_map[device]
        value = Value.ACTIVE if state else Value.INACTIVE
        if reverse:
            value = Value.INACTIVE if value == Value.ACTIVE else Value.ACTIVE
        if self.is_gpio() and self.lines:
            self.lines.set_value(pin, value)
        self._state[device] = state

    def get_gpio_pin(self, device: str) -> int:
        """Get GPIO pin state."""
        return self.pin_map[device]

    def set_gpio_pin(self, device: str, pin: int) -> None:
        self.pin_map[device] = pin
        self.close()
        self.init_gpio_line()

    def close(self) -> None:
        if self.is_gpio() and self.lines:
            self.lines.release()
