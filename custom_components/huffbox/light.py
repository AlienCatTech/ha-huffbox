from typing import ClassVar

from homeassistant.components.light import (
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from numpy import True_

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [HuffBoxLight(entry), HuffBoxLED(entry), HuffUILightTheme(entry)],
        update_before_add=True,
    )


class HuffBoxLight(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_light")

    @property
    def color_mode(self) -> ColorMode | str | None:
        return self._attr_color_mode

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        return self._attr_supported_color_modes

    @property
    def is_on(self) -> bool:
        return self.huffbox.gpio.get_gpio_state("light")

    async def async_turn_on(self) -> None:
        self.huffbox.gpio.set_gpio_state("light", state=True)

    async def async_turn_off(self) -> None:
        self.huffbox.gpio.set_gpio_state("light", state=False)


class HuffBoxLED(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "led")
        self._attr_effect_list = self.huffbox.led.effect_list

    @property
    def is_on(self) -> bool:
        return self.huffbox.led.is_on()

    @property
    def effect(self) -> str:
        return self.huffbox.led.effect

    async def async_turn_on(self, **kwargs: str) -> None:
        self.huffbox.led.turn_on()
        if ATTR_EFFECT in kwargs:
            new_effect = kwargs[ATTR_EFFECT]
            self.huffbox.led.effect = new_effect

    async def async_turn_off(self) -> None:
        self.huffbox.led.turn_off()


class HuffUILightTheme(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.ONOFF}

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_light")
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
