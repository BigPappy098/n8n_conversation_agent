from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import conversation

from .agent import N8NConversationAgent
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    webhook_url = entry.data["webhook_url"]
    agent = N8NConversationAgent(hass, webhook_url)
    conversation.async_set_agent(hass, entry, agent)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    conversation.async_unset_agent(hass, entry)
    return True
