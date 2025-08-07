from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.conversation import async_set_agent, async_unset_agent
from .conversation import N8NConversationAgent
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True  # rely on config flow

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    webhook_url = entry.data.get("webhook_url")
    if not webhook_url:
        _LOGGER.error("Missing webhook_url in config entry: %s", entry.entry_id)
        return False
    agent = N8NConversationAgent(hass, webhook_url)
    async_set_agent(hass, entry, agent)
    _LOGGER.warning("n8n Conversation Agent registered (entry_id=%s)", entry.entry_id)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_unset_agent(hass, entry)
    _LOGGER.warning("n8n Conversation Agent unloaded (entry_id=%s)", entry.entry_id)
    return True
