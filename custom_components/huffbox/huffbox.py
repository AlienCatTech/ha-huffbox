from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.huffbox.glitch import Glitcher
from custom_components.huffbox.media import HuffBoxMediaManager

from .common import countdown_until, get_config_dir
from .gpio import HuffBoxGPIO
from .led import (
    EFFECT_COUNTDOWN,
    EFFECT_CUSTOM_TEXT,
    EFFECT_TIMER,
    sec_to_hms,
)
from .wled import HuffBoxWLED


class HuffBox:
    """Representation of HuffBox."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize HuffBox."""
        self.hass = hass
        self.entry = entry
        self.second_passed = 0
        self.is_locked = False
        self.gpio = HuffBoxGPIO(hass)
        self.pixel_led = HuffBoxWLED(hass, "text.huffbox_wled_pixel_led_ip")
        self.media_manager = HuffBoxMediaManager(hass, get_config_dir(hass) / "media")
        self.glicher = Glitcher(hass)

    def update_second_passed(self) -> int:
        if self.is_locked:
            self.second_passed += 1
        else:
            self.second_passed = 0

        return self.second_passed

    async def update_led(self) -> None:
        match self.pixel_led.effect:
            case e if e == EFFECT_COUNTDOWN:
                future = self.hass.states.get("time.huffbox_time")
                if future:
                    await self.pixel_led.send_text(countdown_until(future.state))
            case e if e == EFFECT_TIMER:
                await self.pixel_led.send_text(sec_to_hms(self.second_passed))
            case e if e == EFFECT_CUSTOM_TEXT:
                custom_text = self.hass.states.get("text.huffbox_custom_led_text")
                if custom_text:
                    await self.pixel_led.send_text(custom_text.state)
            case _:
                return

    async def async_will_remove_from_hass(self) -> None:
        self.close()

    def close(self) -> None:
        self.gpio.close()
