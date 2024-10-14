from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
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
            SceneStudioSensor(entry),
        ],
        update_before_add=True,
    )


class MockSensor(
    HuffBoxBaseEntity,
    CoordinatorEntity,
    SensorEntity,
):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, config_entry: HuffBoxConfigEntry, name: str) -> None:
        super().__init__(config_entry, name)
        CoordinatorEntity.__init__(self, config_entry.runtime_data.random_coordinator)
        self._name = name

    @property
    def native_value(self) -> int:
        return self.coordinator.data[self._name]


class IPSensor(
    HuffBoxBaseEntity,
    SensorEntity,
):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "lan_ip")
        self._state = get_lan_ip()

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self._state


class SceneStudioSensor(
    HuffBoxBaseEntity,
    SensorEntity,
):
    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "scene_studio_current")
        self._state = "idle"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self._state

    async def _handle_update(self, data: str) -> None:
        self._state = data
        self.async_write_ha_state()
        await self.async_update_ha_state()

    async def async_added_to_hass(self) -> None:
        async_dispatcher_connect(
            self.hass, "update_huffbox_scene_studio_current", self._handle_update
        )
