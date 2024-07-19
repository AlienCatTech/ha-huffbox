from homeassistant import config_entries, data_entry_flow

from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class HuffboxConfigFlow(config_entries.ConfigFlow):
    async def async_step_user(self, user_input=None) -> data_entry_flow.FlowResult:  # noqa: ANN001, ARG002
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title=DOMAIN, data={})
