from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from typing import Any
from .const import DOMAIN

class N8NConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """UI configuration for n8n Conversation Agent."""
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({vol.Required("webhook_url"): str}),
            )
        return self.async_create_entry(
            title="n8n Conversation Agent", data={"webhook_url": user_input["webhook_url"]}
        )
