from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from custom_components.huffbox.coordinator import RandomNumberCoordinator

from .huffbox import HuffBox

type HuffBoxConfigEntry = ConfigEntry[HuffBoxData]


@dataclass
class HuffBoxData:
    """Data for the integration."""

    huffbox: HuffBox
    coordinator: RandomNumberCoordinator
