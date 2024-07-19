import time
import traceback
from pathlib import Path
from threading import Event, Thread

from homeassistant.core import HomeAssistant
from PIL import ImageFont

from .const import LOGGER

current_dir = Path(__file__).parent.resolve()
thin_font = (ImageFont.truetype(current_dir / "fonts" / "slkscr.ttf", 8), 7)
normal_font = (
    ImageFont.truetype(current_dir / "fonts" / "pixelmix.ttf", 8),
    6,
)
bold_font = (
    ImageFont.truetype(current_dir / "fonts" / "Super Mario Bros. 2.ttf", 8),
    8,
)


def sec_to_hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"


EFFECT_COUNTDOWN = "Countdown"
EFFECT_TIMER = "Timer"
EFFECT_CUSTOM_TEXT = "Custom Text"


class HuffBoxLED:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.spi_path = "/dev/spidev0.0"
        self.stop_event = Event()
        self.scrolling = False
        self.speed = 0.05
        self.contrast = 1
        self.text = ""
        self.font = normal_font
        self.center = False
        self.effect_list = [EFFECT_TIMER, EFFECT_COUNTDOWN, EFFECT_CUSTOM_TEXT]
        self.effect = self.effect_list[0]
        self._is_hide = False

    async def start(self) -> None:
        if self.is_led():
            await self.hass.async_add_executor_job(self.init_spi)

    def is_led(self) -> bool:
        return Path(self.spi_path).exists()

    def init_spi(self) -> None:
        from luma.core.interface.serial import noop, spi
        from luma.core.virtual import viewport
        from luma.led_matrix.device import max7219

        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(
            self.serial,
            cascaded=4,
            contrast=self.contrast,
            block_orientation=90,
            blocks_arranged_in_reverse_order=True,
        )
        self.virtual = viewport(self.device, width=10000, height=8)
        thread = Thread(target=self.display)
        thread.start()

    def set_font(self, font: str) -> None:
        if font == "normal":
            self.font = normal_font
        elif font == "thin":
            self.font = thin_font
        elif font == "bold":
            self.font = bold_font
        else:
            msg = "no font found"
            raise Exception(msg)

    def is_on(self) -> bool:
        return not self._is_hide

    def turn_on(self) -> None:
        if self.is_led():
            self.device.show()
        self._is_hide = False

    def turn_off(self) -> None:
        if self.is_led():
            self.device.hide()
        self._is_hide = True

    def display(self) -> None:
        from luma.core.render import canvas

        try:
            if not self.is_led() or not hasattr(self, "device"):
                return
            while not self.stop_event.is_set():
                if not self.scrolling:
                    with canvas(self.device) as draw:
                        center_offset = 0
                        if self.center:
                            center_offset = (
                                self.device.width - len(self.text) * self.font[1]
                            ) / 2
                        draw.text(
                            (center_offset, 0),
                            self.text,
                            fill="white",
                            font=self.font[0],
                        )
                    time.sleep(0.5)

                else:
                    with canvas(self.virtual) as draw:
                        draw.text(
                            (self.device.width, 0),
                            self.text,
                            fill="white",
                            font=self.font[0],
                        )
                    for offset in range(
                        len(self.text) * self.font[1] + self.device.width
                    ):
                        if self.stop_event.is_set():
                            break
                        self.virtual.set_position((offset, 0))
                        time.sleep(self.speed)
                    time.sleep(0.01)

        except Exception as e:
            LOGGER.exception(e)
            traceback.print_exc()

    def show_text(
        self,
        text: str,
        scrolling: bool = False,
        font: str = "normal",
        center: bool = False,
        speed: float = 0.05,
    ) -> None:
        self.set_font(font)
        self.scrolling = scrolling
        self.text = text
        self.center = center
        self.speed = speed

    def close(self) -> None:
        self.stop_event.set()
        if self.is_led() and hasattr(self, "device"):
            self.device.cleanup()
