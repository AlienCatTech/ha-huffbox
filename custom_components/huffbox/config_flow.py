from types import MappingProxyType
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .common import GPIO_VALUES
from .const import DOMAIN


def get_value_from_dict(
    dictt: MappingProxyType[str, Any] | None, key: str, default_value: Any
) -> Any:
    if dictt:
        return dictt.get(key, default_value)
    return default_value


def get_gpio_schema(
    config_data: MappingProxyType[str, Any] | None = None,
) -> vol.Schema:
    """Generate the schema for GPIO fields."""
    return vol.Schema(
        {
            vol.Required(
                key,
                default=get_value_from_dict(config_data, key, value),
            ): int
            for key, value in GPIO_VALUES.items()
        }
    )


class HuffboxConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=get_gpio_schema(),
                errors=errors,
            )

        # Validate input here if needed

        return self.async_create_entry(title=DOMAIN, data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=get_gpio_schema(self.config_entry.data),
        )
