from homeassistant.components.text import TextEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities(
        [
            HuffTextEntity(entry, "subject_name"),
            HuffTextEntity(entry, "subject_picture"),
            HuffTextEntity(entry, "custom_layout_link"),
            HuffTextEntity(entry, "custom_led_text"),
            HuffTextEntity(entry, "banner", "WARNING"),
            HuffTextEntity(entry, "live_chat", "live-chat.json"),
            HuffTextEntity(entry, "video_link", "hypno.mp4"),
        ],
        True,
    )


class HuffTextEntity(HuffBoxBaseEntity, RestoreEntity, TextEntity):
    def __init__(
        self, config_entry: HuffBoxConfigEntry, config_name: str, default: str = ""
    ) -> None:
        super().__init__(config_entry, config_name)
        self._state = default

    @property
    def native_value(self):
        return self._state

    async def async_set_value(self, value: str) -> None:
        self._state = value
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
