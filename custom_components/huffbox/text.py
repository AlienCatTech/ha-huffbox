from typing import Any

from homeassistant.components.text import TextEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity
from .huffbox import HuffBox
from .wled import EFFECT_CUSTOM_TEXT


async def set_custom_text_effect(hb: HuffBox, v: str) -> None:
    hb.pixel_led.effect = EFFECT_CUSTOM_TEXT
    await hb.pixel_led.send_text(v)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            HuffTextEntity(entry, "subject_name"),
            HuffTextEntity(entry, "subject_picture"),
            HuffTextEntity(entry, "custom_layout_link", category=EntityCategory.CONFIG),
            HuffTextEntity(
                entry,
                "custom_led_text",
                set_cb=lambda hb, v: set_custom_text_effect(hb, v),
            ),
            HuffTextEntity(entry, "banner", "WARNING", category=EntityCategory.CONFIG),
            HuffTextEntity(
                entry, "live_chat", "live-chat.json", category=EntityCategory.CONFIG
            ),
            HuffTextEntity(
                entry, "video_link", "hypno.mp4", category=EntityCategory.CONFIG
            ),
            HuffTextEntity(entry, "wled_pixel_led_ip", category=EntityCategory.CONFIG),
            HuffTextEntity(
                entry, "wled_ambient_light_ip", category=EntityCategory.CONFIG
            ),
        ],
        update_before_add=True,
    )


class HuffTextEntity(HuffBoxBaseEntity, RestoreEntity, TextEntity):
    def __init__(
        self,
        config_entry: HuffBoxConfigEntry,
        config_name: str,
        default: str = "",
        category: EntityCategory | None = None,
        set_cb: Any = None,
        get_cb: Any = None,
    ) -> None:
        super().__init__(config_entry, config_name)
        self._state = default
        if category:
            self._attr_entity_category = category
        self.set_cb = set_cb
        self.get_cb = get_cb

    @property
    def native_value(self) -> str:
        if self.get_cb:
            return self.get_cb(self.huffbox)
        return self._state

    async def async_set_value(self, value: str) -> None:
        if self.set_cb is not None:
            await self.set_cb(self.huffbox, value)
        self._state = value
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
