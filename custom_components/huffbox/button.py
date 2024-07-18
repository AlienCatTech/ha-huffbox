from homeassistant.components.button import ButtonEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities([HuffBoxButton(entry)], True)


class HuffBoxButton(HuffBoxBaseEntity, ButtonEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "refresh_button")

    async def async_press(self) -> None:
        """Handle the button press."""
        self.hass.bus.async_fire("huffbox_refresh_event")
