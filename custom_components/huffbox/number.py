from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities(
        [
            GPIOPinEntity(entry, "light"),
            GPIOPinEntity(entry, "fan"),
            GPIOPinEntity(entry, "lock"),
        ],
        True,
    )


class GPIOPinEntity(HuffBoxBaseEntity, RestoreEntity, NumberEntity):
    _attr_native_step = 1.0

    def __init__(self, config_entry: HuffBoxConfigEntry, switch_name: str) -> None:
        super().__init__(config_entry, f"gpio_pin_{switch_name}")
        self.switch_name = switch_name

    @property
    def native_value(self):
        return self.huffbox.gpio.get_gpio_pin(self.switch_name)

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        self.huffbox.gpio.set_gpio_pin(self.switch_name, int(value))

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            await self.async_set_native_value(int(state.state))
