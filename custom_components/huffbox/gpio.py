from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .common import GPIO_VALUES
from .const import NAME


class HuffBoxGPIO:
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self.hass = hass
        self.lines = None
        self.pin_map = {
            "lock": int(config_entry.data.get("lock_gpio", GPIO_VALUES["lock_gpio"])),
            "fan": config_entry.data.get("fan_gpio", GPIO_VALUES["fan_gpio"]),
            "light": config_entry.data.get("light_gpio", GPIO_VALUES["light_gpio"]),
        }
        self._state = {"lock": False, "fan": False, "light": True}
        self.reverse_map = {"lock": False, "fan": False, "light": True}
        self.chip_name = "/dev/gpiochip4"

    async def start(self) -> None:
        if self.is_gpio():
            await self.hass.async_add_executor_job(self.init_gpio_line)

    def is_gpio(self) -> bool:
        return Path(self.chip_name).exists()

    def init_gpio_line(self) -> None:
        import gpiod

        if self.is_gpio():
            config = {
                self.pin_map[x]: gpiod.LineSettings(
                    direction=gpiod.line.Direction.OUTPUT
                )
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
        from gpiod.line import Value

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
