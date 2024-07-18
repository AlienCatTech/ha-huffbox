from homeassistant.components.light import (
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities([HuffBoxLight(entry), HuffBoxLED(entry)], True)


class HuffBoxLight(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "control_light")

    @property
    def color_mode(self):
        return self._attr_color_mode

    @property
    def supported_color_modes(self):
        return self._attr_supported_color_modes

    @property
    def is_on(self):
        return self.huffbox.gpio.get_gpio_state("light")

    async def async_turn_on(self, **kwargs):
        self.huffbox.gpio.set_gpio_state("light", True)

    async def async_turn_off(self, **kwargs):
        self.huffbox.gpio.set_gpio_state("light", False)


class HuffBoxLED(HuffBoxBaseEntity, LightEntity):
    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "led")
        self._attr_effect_list = self.huffbox.led.effect_list

    @property
    def is_on(self):
        return self.huffbox.led.is_on()

    @property
    def effect(self):
        return self.huffbox.led.effect

    async def async_turn_on(self, **kwargs):
        self.huffbox.led.turn_on()
        if ATTR_EFFECT in kwargs:
            new_effect = kwargs[ATTR_EFFECT]
            self.huffbox.led.effect = new_effect

    async def async_turn_off(self, **kwargs):
        self.huffbox.led.turn_off()
