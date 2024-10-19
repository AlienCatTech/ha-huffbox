from collections.abc import Callable
from io import BytesIO
from pathlib import Path

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.huffbox.common import get_config_dir, www_to_link
from custom_components.huffbox.huffbox import HuffBox

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def trigger_glitcher(hass: HomeAssistant, huffbox: HuffBox) -> None:
    picture_state = "text.huffbox_subject_picture"
    pic_url = hass.states.get(picture_state)
    if pic_url:
        session = async_get_clientsession(hass)
        url = pic_url.state
        if "http" not in url:
            url = "http://localhost:8123" + url
        async with session.get(url) as response:
            ok_status = 200
            if response.status == ok_status:
                output = (
                    get_config_dir(hass)
                    / "www"
                    / (str(Path(pic_url.state).parent.name) + ".gif")
                )
                data = await response.read()
                await huffbox.glicher.glitch_img(BytesIO(data), output)
                await hass.services.async_call(
                    "text",
                    "set_value",
                    {"value": www_to_link(hass, output)},
                    target={"entity_id": picture_state},
                )
            else:
                return


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            HuffBoxButton(
                entry,
                "refresh",
                press_cb=lambda hass, _: hass.bus.async_fire("huffbox_refresh_event"),
                is_config=True,
            ),
            HuffBoxButton(
                entry,
                "glitcher",
                press_cb=lambda hass, huffbox: trigger_glitcher(hass, huffbox),
                is_config=True,
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
