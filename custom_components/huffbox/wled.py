import contextlib
import json
from typing import Any

import httpx
from homeassistant.core import HomeAssistant

from custom_components.huffbox.const import LOGGER

HTTP_OK_STATUS = 200
EFFECT_COUNTDOWN = "Countdown"
EFFECT_TIMER = "Timer"
EFFECT_CUSTOM_TEXT = "Custom Text"


class HuffBoxWLED:
    def __init__(self, hass: HomeAssistant, state_name: str) -> None:
        self.hass = hass
        self.wled_id = None
        self.state_name = state_name
        self.text_speed = 255
        self.text_size = 1
        self.text = ""
        self.effect_list = [
            EFFECT_TIMER,
            EFFECT_COUNTDOWN,
            EFFECT_CUSTOM_TEXT,
        ]
        self.effect = self.effect_list[0]

    async def _get_wled_id(self) -> str | None:
        if self.wled_id:
            return self.wled_id

        name = self.hass.states.get(self.state_name)
        if name:
            try_name = name.state.replace("-", "_")
            ip = self.hass.states.get(f"sensor.{try_name}_ip")
            if ip:
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        response = await client.get(
                            f"http://{ip.state}/json/info", timeout=10
                        )
                        if response.status_code == HTTP_OK_STATUS:
                            j = response.json()
                            mac = j.get("mac")
                            if mac:
                                self.wled_id = mac[-6:]
                                return self.wled_id
                except httpx.ConnectError:
                    pass
                except Exception as e:
                    LOGGER.error(
                        f"failed to send mqtt to wled - {ip.state}: ", exc_info=e
                    )

        return None

    async def send_data(self, body: Any) -> None:
        wled_id = await self._get_wled_id()
        with contextlib.suppress(Exception):
            await self.hass.services.async_call(
                "mqtt",
                "publish",
                service_data={
                    "topic": f"wled/{wled_id}/api",
                    "payload": json.dumps(body),
                },
            )

    async def send_text(self, text: str) -> None:
        if text == self.text:
            return
        self.text = text
        body = {
            "seg": [
                {
                    "fx": 122,  # scroll text
                    "sx": 255,  # speed
                    "ix": 128,  # y offset
                    "c1": 1,  # trail
                    "n": text,  # text
                }
            ]
        }
        await self.send_data(body)

    async def send_text_size(self, size: int) -> None:
        if size == self.text_size:
            return
        self.text_size = size
        body = {
            "seg": [
                {
                    "fx": 122,  # scroll text
                    "sx": 255,  # speed
                    "ix": 128,  # y offset
                    "grp": size,  # grouping/font size
                    "c1": 1,  # trail
                }
            ]
        }
        await self.send_data(body)

    async def send_text_speed(self, speed: int) -> None:
        if speed == self.text_speed:
            return
        self.text_speed = speed
        body = {
            "seg": [
                {
                    "fx": 122,  # scroll text
                    "sx": speed,  # speed
                    "ix": 128,  # y offset
                    "c1": 1,  # trail
                }
            ]
        }
        await self.send_data(body)

    async def send_effect(
        self,
        effect: int,
        segment: int = 1,
        sx: int | None = None,
        ix: int | None = None,
        c1: int | None = None,
        c2: int | None = None,
        c3: int | None = None,
    ) -> None:
        body = {
            "seg": [
                {
                    "fx": effect,
                    "sx": sx,
                    "ix": ix,
                    "c1": c1,
                    "c2": c2,
                    "c3": c3,
                }
                for _ in range(segment)
            ]
        }

        body = {k: v for k, v in body.items() if v is not None}

        await self.send_data(body)
