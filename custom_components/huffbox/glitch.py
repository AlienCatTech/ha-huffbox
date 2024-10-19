from io import BytesIO
from pathlib import Path
from typing import IO

from glitch_this import ImageGlitcher
from homeassistant.core import HomeAssistant
from PIL import Image, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Glitcher:
    def __init__(self, hass: HomeAssistant) -> None:
        self.glitcher = ImageGlitcher()
        self.hass = hass

    async def glitch_img(self, img: str | IO[bytes], output: Path) -> None:
        return await self.hass.async_add_executor_job(self._glitch_img, img, output)

    def _glitch_img(self, img: str | IO[bytes], output: Path) -> None:
        image = Image.open(img)
        rgb_img = ImageOps.exif_transpose(image)
        if not rgb_img:
            return
        rgb_img = rgb_img.convert("RGB")
        rgb_img.thumbnail((800, 800))
        buffer = BytesIO()
        rgb_img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)
        image = Image.open(buffer)
        out = self.glitcher.glitch_image(
            src_img=image, glitch_amount=3, color_offset=True, gif=True
        )
        out[0].save(
            output,
            format="GIF",
            append_images=out[1:],
            save_all=True,
            duration=200,
            loop=0,
        )
