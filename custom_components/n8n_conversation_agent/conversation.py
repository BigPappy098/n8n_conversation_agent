import aiohttp
import logging
from homeassistant.components.conversation import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class SimpleConversationResponse:
    """Minimal conversation response with both .speech and .as_dict() for HA."""
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
        return ["en"]

    async def async_prepare(self, language: str | None = None) -> None:
        pass

    async def async_process(self, input: ConversationInput) -> ConversationResult:
        user_text = input.text
        _LOGGER.warning(f"[n8n_agent] Sending to n8n: {user_text}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json={"text": user_text},
                    timeout=15,
                ) as resp:
                    data = await resp.json(content_type=None)
                    _LOGGER.warning(f"[n8n_agent] Raw n8n JSON: {data}")

                    response_text = data.get("response", "")

                    if isinstance(response_text, dict):
                        _LOGGER.warning("[n8n_agent] 'response' is dict — flattening")
                        response_text = (
                            response_text.get("content")
                            or response_text.get("text")
                            or str(response_text)
                        )

                    if not isinstance(response_text, str):
                        _LOGGER.warning("[n8n_agent] 'response' is not string — forcing str()")
                        response_text = str(response_text)

                    if not response_text.strip():
                        _LOGGER.warning("[n8n_agent] Empty response from n8n, using fallback")
                        response_text = "Sorry, I didn't get a response from n8n."

                    _LOGGER.warning(f"[n8n_agent] Final response_text to HA: {response_text!r}")

                    ha_response = SimpleConversationResponse(response_text)
                    return ConversationResult(response=ha_response)

        except Exception as e:
            _LOGGER.error(f"[n8n_agent] Error contacting n8n: {e}")
            ha_response = SimpleConversationResponse("Sorry, I couldn't reach n8n.")
            return ConversationResult(response=ha_response)
