"""HuffBoxEntity class."""

from homeassistant.helpers.device_registry import DeviceInfo

from .common import snake_to_title
from .const import DOMAIN, NAME
from .data import HuffBoxConfigEntry


class HuffBoxBaseEntity:
    """BlueprintEntity class."""

    def __init__(self, config_entry: HuffBoxConfigEntry, config_name: str) -> None:
        self.config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_" + config_name
        self._attr_name = f"{NAME} " + snake_to_title(config_name)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=NAME,
            manufacturer="Alien Cat Techology",
            model="HuffBox v1.0",
            sw_version="1.0.0",
        )
        self.huffbox = config_entry.runtime_data.huffbox
        self._state = ""
