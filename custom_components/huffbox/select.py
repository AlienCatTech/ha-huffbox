from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            HuffBoxSelect(
                entry,
                "select_dashboard",
                [
                    "default",
                    "custom",
                    "fullscreen-image",
                    "fullscreen-text",
                    "fullscreen-video",
                ],
            ),
        ],
        update_before_add=True,
    )


class HuffBoxSelect(HuffBoxBaseEntity, RestoreEntity, SelectEntity):
    def __init__(
        self,
        config_entry: HuffBoxConfigEntry,
        name: str,
        options: list,
    ) -> None:
        super().__init__(config_entry, name)
        self.dashboard_options = options
        self._current = self.dashboard_options[0]

    @property
    def current_option(self) -> str:
        return self._current

    @property
    def options(self) -> list[str]:
        return self.dashboard_options

    async def async_select_option(self, option: str) -> None:
        self._current = option
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._current = state.state
