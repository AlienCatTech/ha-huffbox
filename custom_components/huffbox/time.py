from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HuffBoxTime(entry)], update_before_add=True)


class HuffBoxTime(HuffBoxBaseEntity, TimeEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "time")

        self._state = None

    @property
    def native_value(self) -> time | None:
        return self._state

    async def async_set_value(self, value: time) -> None:
        self._state = value
