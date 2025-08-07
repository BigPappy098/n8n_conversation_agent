import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)
CONF_WEBHOOK_URL = "webhook_url"

class N8nConversationAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for N8N Conversation Agent."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial setup step."""
        errors = {}
        if user_input is None:
            # Show the form to input the webhook URL
            data_schema = vol.Schema({vol.Required(CONF_WEBHOOK_URL): str})
            return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

        # Validate and process the submitted webhook URL
        webhook = user_input.get(CONF_WEBHOOK_URL, "").strip()
        if not webhook.lower().startswith(("http://", "https://")):
            errors["base"] = "invalid_url"
        else:
            # Check if this webhook URL is already configured
            for existing_entry in self._async_current_entries():
                if existing_entry.data.get(CONF_WEBHOOK_URL) == webhook:
                    return self.async_abort(reason="already_configured")
            # Optionally, attempt a test connection (omitted here for simplicity)
            if not errors:
                # Create the config entry
                _LOGGER.debug("Creating N8N Conversation Agent entry for webhook: %s", webhook)
                return self.async_create_entry(title="N8N Conversation", data={CONF_WEBHOOK_URL: webhook})

        # Show the form again if there were errors
        data_schema = vol.Schema({vol.Required(CONF_WEBHOOK_URL): str})
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
