from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.huffbox.common import get_lan_ip

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass, entry: HuffBoxConfigEntry, async_add_entities
) -> None:
    async_add_entities(
        [
            MockSensor(entry, "heart_rate"),
            MockSensor(entry, "pulse"),
            MockSensor(entry, "spo2"),
            MockSensor(entry, "resp"),
            MockSensor(entry, "temp"),
            SecondPassedSensor(entry),
            IPSensor(entry),
        ],
        True,
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
    def native_value(self):
        return self.coordinator.data[self._name]


class SecondPassedSensor(
    HuffBoxBaseEntity,
    SensorEntity,
):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "second_passed")
        self._state = 0

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.huffbox.second_passed


class IPSensor(
    HuffBoxBaseEntity,
    SensorEntity,
):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "lan_ip")
        self._state = get_lan_ip()

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state
