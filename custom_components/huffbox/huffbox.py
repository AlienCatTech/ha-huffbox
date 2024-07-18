from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.huffbox.common import countdown_until

from .gpio import HuffBoxGPIO
from .led import (
    EFFECT_COUNTDOWN,
    EFFECT_CUSTOM_TEXT,
    EFFECT_TIMER,
    HuffBoxLED,
    sec_to_hms,
)


class HuffBox:
    """Representation of HuffBox."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize HuffBox."""
        self.hass = hass
        self.entry = entry
        self.second_passed = 0
        self.is_locked = False
        self.gpio = HuffBoxGPIO()
        self.led = HuffBoxLED(hass)

    def update_second_passed(self):
        if self.is_locked:
            self.second_passed += 1
        else:
            self.second_passed = 0

        if self.led.is_on():
            if self.led.effect == EFFECT_TIMER:
                self.led.show_text(sec_to_hms(self.second_passed))
            elif self.led.effect == EFFECT_COUNTDOWN:
                future = self.hass.states.get("time.huffbox_time")
                if future:
                    self.led.show_text(countdown_until(future.state))
            elif self.led.effect == EFFECT_CUSTOM_TEXT:
                custom_text = self.hass.states.get("text.huffbox_custom_led_text")
                if custom_text:
                    self.led.show_text(custom_text.state, True)

    async def async_will_remove_from_hass(self):
        self.close()

    def close(self, event=None):
        self.gpio.close()
        self.led.close()
