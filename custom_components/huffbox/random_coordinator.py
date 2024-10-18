import random
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import LOGGER
from .huffbox import HuffBox


class RandomNumberCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, huffbox: HuffBox) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            logger=LOGGER,
            name="Random Number Sensor",
            update_interval=timedelta(seconds=1),
        )
        self.huffbox = huffbox

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        await self.huffbox.update_led()
        return {
            "second_passed": self.huffbox.update_second_passed(),
            "media_player_second_passed": lambda x: x(),
            "heart_rate": random.randint(70, 90),
            "pulse": random.randint(70, 90),
            "spo2": random.randint(90, 99),
            "resp": random.randint(20, 30),
            "temp": random.randint(96, 100),
        }
