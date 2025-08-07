from homeassistant.components.conversation import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant
from homeassistant.const import MATCH_ALL

from .const import DOMAIN

import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)


class SimpleConversationResponse:
    def __init__(self, text: str) -> None:
        self.speech = {
            "plain": {
                "speech": text,
                "extra_data": None
            }
        }

    def as_dict(self) -> dict:
        return {"speech": self.speech}


class N8NConversationAgent(AbstractConversationAgent):
    def __init__(self, hass: HomeAssistant, webhook_url: str) -> None:
        self.hass = hass
        self.webhook_url = webhook_url

    @property
    def attribution(self) -> str:
        return "Powered by n8n"

    @property
    def supported_languages(self) -> list[str]:
        return [MATCH_ALL]

    async def async_prepare(self, language: str | None = None) -> None:
        pass

    async def async_process(self, input: ConversationInput) -> ConversationResult:
        user_text = input.text
        _LOGGER.debug(f"[n8n_agent] Sending to n8n: {user_text}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json={"text": user_text},
                    timeout=15,
                ) as resp:
                    data = await resp.json(content_type=None)
                    _LOGGER.debug(f"[n8n_agent] Raw n8n JSON: {data}")

                    response_text = data.get("response", "")

                    if isinstance(response_text, dict):
                        response_text = (
                            response_text.get("content")
                            or response_text.get("text")
                            or str(response_text)
                        )

                    if not isinstance(response_text, str):
                        response_text = str(response_text)

                    if not response_text.strip():
                        response_text = "Sorry, I didn't get a response from n8n."

                    return ConversationResult(response=SimpleConversationResponse(response_text))

        except Exception as e:
            _LOGGER.error(f"[n8n_agent] Error contacting n8n: {e}")
            return ConversationResult(response=SimpleConversationResponse("Sorry, I couldn't reach n8n."))


async def async_get_agent(hass: HomeAssistant, config: dict) -> AbstractConversationAgent:
    entry = next(iter(hass.config_entries.async_entries(DOMAIN)), None)
    if not entry:
        raise ValueError("n8n agent not configured.")
    webhook_url = entry.data.get("webhook_url")
    return N8NConversationAgent(hass, webhook_url)
