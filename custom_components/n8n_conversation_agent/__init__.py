import logging
from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "n8n_conversation_agent"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the N8N Conversation Agent integration from a config entry."""
    # No platforms to set up; just indicate successful setup.
    _LOGGER.debug("Setting up N8N Conversation Agent entry: %s", entry.title)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the N8N Conversation Agent integration."""
    _LOGGER.debug("Unloading N8N Conversation Agent entry: %s", entry.title)
    # Unregister the conversation agent if registered
    conversation.async_unset_agent(hass, entry)
    return True

async def async_get_conversation_agent(hass: HomeAssistant, config_entry: ConfigEntry):
    """Entry point for Assist to get the conversation agent instance."""
    from .conversation import N8nConversationAgent
    return N8nConversationAgent(hass, config_entry)
