from typing import ClassVar

from homeassistant.components.light import (
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [HuffBoxStripLights(entry), HuffBoxInternalLED(entry), HuffUILightTheme(entry)],
        update_before_add=True,
    )


class HuffBoxStripLights(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "strip_light")

    @property
    def color_mode(self) -> ColorMode | str | None:
        return self._attr_color_mode

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        return self._attr_supported_color_modes

    @property
    def is_on(self) -> bool:
        return self.huffbox.gpio.get_gpio_state("strip")

    async def async_turn_on(self) -> None:
        self.huffbox.gpio.set_gpio_state("strip", state=True)

    async def async_turn_off(self) -> None:
        self.huffbox.gpio.set_gpio_state("strip", state=False)


class HuffBoxInternalLED(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "internal_led")
        self._attr_effect_list = self.huffbox.internal_led.effect_list

    @property
    def is_on(self) -> bool:
        return self.huffbox.gpio.get_gpio_state("led")

    @property
    def effect(self) -> str:
        return self.huffbox.internal_led.effect

    async def async_turn_on(self, **kwargs: str) -> None:
        self.huffbox.gpio.set_gpio_state("led", state=True)
        if ATTR_EFFECT in kwargs:
            new_effect = kwargs[ATTR_EFFECT]
            self.huffbox.internal_led.effect = new_effect

    async def async_turn_off(self) -> None:
        self.huffbox.gpio.set_gpio_state("led", state=False)


class HuffUILightTheme(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "huffui_lightmode")
        self.isLightTheme = True

    @property
    def color_mode(self) -> ColorMode | str | None:
        return self._attr_color_mode

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        return self._attr_supported_color_modes

    @property
    def is_on(self) -> bool:
        return self.isLightTheme

    async def async_turn_on(self) -> None:
        self.isLightTheme = True

    async def async_turn_off(self) -> None:
        self.isLightTheme = False
