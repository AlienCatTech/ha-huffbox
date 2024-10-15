from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            GPIOPinEntity(entry, "strip"),
            GPIOPinEntity(entry, "fan"),
            GPIOPinEntity(entry, "lock"),
            HuffBoxNumberEntity(
                entry,
                "text_speed",
                default=255,
                get_cb=lambda hb: hb.internal_led.text_speed,
                set_cb=lambda hb, v: hb.internal_led.send_text_speed(v),
            ),
            HuffBoxNumberEntity(
                entry,
                "text_size",
                default=1,
                get_cb=lambda hb: hb.internal_led.text_size,
                set_cb=lambda hb, v: hb.internal_led.send_text_size(v),
                native_min_value=1,
                native_max_value=4,
            ),
        ],
        update_before_add=True,
    )


class HuffBoxNumberEntity(HuffBoxBaseEntity, NumberEntity):
    _attr_native_step = 1.0

    def __init__(
        self,
        config_entry: HuffBoxConfigEntry,
        name: str,
        default: int = 0,
        set_cb: Any = None,
        get_cb: Any = None,
        native_max_value: int = 255,
        native_min_value: int = 0,
    ) -> None:
        super().__init__(config_entry, name)
        self._state = default
        self.config_entry = config_entry
        self.set_cb = set_cb
        self.get_cb = get_cb
        self.native_max_value = native_max_value
        self.native_min_value = native_min_value

    @property
    def native_value(self) -> int:
        if self.get_cb:
            return self.get_cb(self.huffbox)
        return self._state

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        if self.set_cb:
            await self.set_cb(self.huffbox, int(value))
        self._state = int(value)


class GPIOPinEntity(HuffBoxBaseEntity, RestoreEntity, NumberEntity):
    _attr_native_step = 1.0

    def __init__(self, config_entry: HuffBoxConfigEntry, switch_name: str) -> None:
        super().__init__(config_entry, f"gpio_pin_{switch_name}")
        self.switch_name = switch_name
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def native_value(self) -> int:
        return self.huffbox.gpio.get_gpio_pin(self.switch_name)

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        self.huffbox.gpio.set_gpio_pin(self.switch_name, int(value))

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            await self.async_set_native_value(int(state.state))
