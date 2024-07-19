from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HuffBoxLock(entry)], update_before_add=True)


class HuffBoxLock(HuffBoxBaseEntity, LockEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_lock")

    @property
    def is_locked(self) -> bool:
        return self.huffbox.gpio.get_gpio_state("lock")

    async def async_lock(self) -> None:
        self.huffbox.is_locked = True
        self.huffbox.gpio.set_gpio_state("lock", state=True)

    async def async_unlock(self) -> None:
        self.huffbox.is_locked = False
        self.huffbox.gpio.set_gpio_state("lock", state=False)
