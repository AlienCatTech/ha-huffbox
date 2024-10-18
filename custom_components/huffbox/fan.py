from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HuffBoxFan(entry)], update_before_add=True)


class HuffBoxFan(HuffBoxBaseEntity, FanEntity):
    _attr_supported_features = FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_fan")

    @property
    def is_on(self) -> bool:
        return self.huffbox.gpio.get_gpio_state("fan")

    async def async_turn_on(
        self,
        speed: str | None = None,  # noqa: ARG002
        percentage: int | None = None,  # noqa: ARG002
        preset_mode: str | None = None,  # noqa: ARG002
    ) -> None:
        self.huffbox.gpio.set_gpio_state("fan", state=True)

    async def async_turn_off(self) -> None:
        self.huffbox.gpio.set_gpio_state("fan", state=False)
