from homeassistant import config_entries

from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class HuffboxConfigFlow(config_entries.ConfigFlow):
    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title=DOMAIN, data={})


#     @staticmethod
#     @callback
#     def async_get_options_flow(config_entry):
#         return HuffboxEditFlow(config_entry)


# class HuffboxEditFlow(config_entries.OptionsFlow):
#     def __init__(self, config_entry:HuffBoxConfigEntry) -> None:
#         self.config_entry = config_entry

#     async def async_step_init(self, user_input=None):
#         if user_input is not None:
#             return self.async_create_entry(title=DOMAIN, data=user_input)

#         schema = {
#             vol.Optional(LAYOUT_CONFIG, default=self.config_entry.options.get(LAYOUT_CONFIG, "{}")): str,
#         }

#         return self.async_show_form(
#             step_id="init",
#             data_schema=vol.Schema(schema)
#         )
