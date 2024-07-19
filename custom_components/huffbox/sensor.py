from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.huffbox.common import get_lan_ip

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            MockSensor(entry, "heart_rate"),
            MockSensor(entry, "pulse"),
            MockSensor(entry, "spo2"),
            MockSensor(entry, "resp"),
            MockSensor(entry, "temp"),
            MockSensor(entry, "second_passed"),
            IPSensor(entry),
        ],
        update_before_add=True,
    )


class MockSensor(
    HuffBoxBaseEntity,
    CoordinatorEntity,
    SensorEntity,
):
    def __init__(self, config_entry: HuffBoxConfigEntry, name: str) -> None:
        super().__init__(config_entry, name)
        CoordinatorEntity.__init__(self, config_entry.runtime_data.coordinator)
        self._name = name

    @property
    def native_value(self) -> int:
        return self.coordinator.data[self._name]


class IPSensor(
    HuffBoxBaseEntity,
    SensorEntity,
):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "lan_ip")
        self._state = get_lan_ip()

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self._state
