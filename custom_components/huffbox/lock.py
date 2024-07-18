from homeassistant.components.lock import LockEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities([HuffBoxLock(entry)], True)


class HuffBoxLock(HuffBoxBaseEntity, LockEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_lock")

    @property
    def is_locked(self):
        return self.huffbox.gpio.get_gpio_state("lock")

    async def async_lock(self, **kwargs):
        self.huffbox.is_locked = True
        return self.huffbox.gpio.set_gpio_state("lock", True)

    async def async_unlock(self, **kwargs):
        self.huffbox.is_locked = False
        return self.huffbox.gpio.set_gpio_state("lock", False)
