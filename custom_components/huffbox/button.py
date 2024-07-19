from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HuffBoxButton(entry)], update_before_add=True)


class HuffBoxButton(HuffBoxBaseEntity, ButtonEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "refresh_button")

    async def async_press(self) -> None:
        """Handle the button press."""
        self.hass.bus.async_fire("huffbox_refresh_event")
