import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class N8NConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="n8n Conversation Agent",
                data={"webhook_url": user_input["webhook_url"]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("webhook_url"): str
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return N8NOptionsFlow(config_entry)


class N8NOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={"webhook_url": user_input["webhook_url"]}
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "webhook_url",
                    default=self.config_entry.options.get("webhook_url") or self.config_entry.data.get("webhook_url", "")
                ): str
            })
        )
