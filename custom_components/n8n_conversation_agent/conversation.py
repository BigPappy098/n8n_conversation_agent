import logging
from typing import Literal

from homeassistant.components import conversation
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import aiohttp_client, intent
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.device_registry as dr

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

class N8nConversationAgent(conversation.ConversationEntity):
    """Conversation agent that forwards queries to an N8N webhook."""

    # This agent can control Home Assistant (allow Assist to forward commands)
    _attr_supported_features = conversation.ConversationEntityFeature.CONTROL

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the N8N conversation agent."""
        self.hass = hass
        self._entry = config_entry
        self.webhook_url = config_entry.data.get("webhook_url")
        # Unique ID for the conversation agent entity
        self._attr_unique_id = config_entry.entry_id
        # Name of the agent (shown in UI dropdown)
        self._attr_name = config_entry.title or "N8N Conversation"
        # Mark all languages as supported
        self._attr_supported_languages: list[str] | Literal["*"] = "*"
        # Register a device in HA for this agent (optional, for device registry visibility)
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.title or "N8N Conversation Agent",
            manufacturer="N8N",
            model="Conversation Webhook"
        )

    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> conversation.ConversationResult:
        """Handle an incoming conversation text by calling the N8N webhook."""
        query_text = user_input.text
        _LOGGER.debug("Forwarding user query to N8N webhook: %s", query_text)
        try:
            # Make an HTTP POST request to the configured N8N webhook with the query
            session = aiohttp_client.async_get_clientsession(self.hass)
            resp = await session.post(self.webhook_url, json={
                "query": query_text,
                "conversation_id": user_input.conversation_id
            })
            if resp.status != 200:
                _LOGGER.error("N8N webhook call failed with status %s", resp.status)
                raise HomeAssistantError(f"Webhook response status: {resp.status}")
            # Try to get response text (JSON or plain text)
            try:
                data = await resp.json(content_type=None)
            except ValueError:
                # If response is not JSON, use plain text
                answer_text = await resp.text()
            else:
                # Handle JSON response structure
                if isinstance(data, dict) and "answer" in data:
                    answer_text = str(data["answer"])
                elif isinstance(data, str):
                    answer_text = data
                else:
                    # Fallback: convert entire JSON to string
                    answer_text = str(data)
            if not answer_text:
                raise HomeAssistantError("Empty response from N8N webhook")
        except Exception as err:
            _LOGGER.error("Error in N8N conversation agent: %s", err)
            # Raising HomeAssistantError will signal an "intent-failed" in pipeline
            raise HomeAssistantError(f"N8N agent failure: {err}") from err

        # Create an intent response with the answer text
        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech(answer_text)
        # Return the conversation result (no multi-turn support, so conversation_id=None)
        return conversation.ConversationResult(
            conversation_id=None,
            response=response,
            continue_conversation=False
        )
