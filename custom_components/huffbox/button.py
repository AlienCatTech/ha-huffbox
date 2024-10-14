from collections.abc import Callable

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity
from .huffbox import HuffBox


async def start_scene(ha: HomeAssistant, hb: HuffBox) -> None:
    s = ha.states.get("select.huffbox_select_scene_studio_preset")
    if s:
        await hb.scene_studio.start(s.state)


async def stop_scene(_: HomeAssistant, hb: HuffBox) -> None:
    hb.scene_studio.stop()


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            HuffBoxButton(
                entry,
                "refresh_button",
                press_cb=lambda hass, _: hass.bus.async_fire("huffbox_refresh_event"),
                is_config=True,
            ),
            HuffBoxButton(
                entry,
                "start_scene_studio",
                press_cb=lambda ha, hb: start_scene(ha, hb),
            ),
            HuffBoxButton(
                entry,
                "stop_scene_studio",
                press_cb=lambda ha, hb: stop_scene(ha, hb),
            ),
        ],
        update_before_add=True,
    )


class HuffBoxButton(HuffBoxBaseEntity, ButtonEntity):
    def __init__(
        self,
        config_entry: HuffBoxConfigEntry,
        name: str = "",
        press_cb: Callable | None = None,
        is_config: bool = False,
    ) -> None:
        super().__init__(config_entry, name)
        self.config_entry = config_entry
        self.press_cb = press_cb
        if is_config:
            self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.press_cb:
            await self.press_cb(self.hass, self.huffbox)
