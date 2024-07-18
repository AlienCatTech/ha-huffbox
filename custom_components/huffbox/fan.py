from typing import Any

from homeassistant.components.fan import FanEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities([HuffBoxFan(entry)], True)


class HuffBoxFan(HuffBoxBaseEntity, FanEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_fan")

    @property
    def is_on(self):
        return self.huffbox.gpio.get_gpio_state("fan")

    async def async_turn_on(
        self,
        speed: str | None = None,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        return self.huffbox.gpio.set_gpio_state("fan", True)

    async def async_turn_off(self, **kwargs):
        return self.huffbox.gpio.set_gpio_state("fan", False)
