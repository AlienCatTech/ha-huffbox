from homeassistant.components.select import SelectEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities([HuffBoxSelect(entry)], True)


class HuffBoxSelect(HuffBoxBaseEntity, SelectEntity):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "select_dashboard")
        self.dashboard_options = [
            "default",
            "custom",
            "fullscreen-image",
            "fullscreen-text",
            "fullscreen-video",
        ]
        self._current = self.dashboard_options[0]

    @property
    def current_option(self):
        return self._current

    @property
    def options(self):
        return self.dashboard_options

    async def async_select_option(self, option: str) -> None:
        self._current = option
