# n8n Conversation Agent

Home Assistant conversation agent that sends all input to an n8n webhook.

## Installation (HACS)
1. Add this repository to HACS as a custom repository.
2. Install the integration.
3. Restart Home Assistant.
4. Go to Settings → Devices & Services → Add Integration → Search for "n8n Conversation Agent".
5. Enter your n8n webhook URL.

## Usage
Once set as your conversation agent in the Assist pipeline, all text/voice queries will be sent to your n8n workflow.
