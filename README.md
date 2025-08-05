# 🗣️ n8n Conversation Agent for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/)

Bring the full power of **n8n automation** into **Home Assistant's Assist** voice/text pipelines.  
This integration lets you set **n8n** as your Conversation Agent — so **every** query to Assist is routed through your n8n workflow and responded to in real time.

---

## ✨ Features

- 🌍 **Multi-language** support — works with any language in Assist (via `MATCH_ALL`).
- 🔌 **Plug-and-play** — set your webhook URL in the UI, no YAML required.
- 🛠 **Fully customizable** — connect to AI models, databases, APIs, or any n8n automation.
- ⚡ **Fast responses** — direct webhook connection between Home Assistant and n8n.
- 📦 **HACS-ready** — install in seconds.

---

## 📸 How it Works

```text
[Home Assistant Assist]
       │
       ▼
[This Integration] → Calls your n8n Webhook → n8n Workflow processes → Sends reply
       ▲
       └────────────── Returns response to Assist for speech/text output
```

---

## 📥 Installation

### 🔹 **HACS (Recommended)**
1. Open **HACS** in Home Assistant.
2. Go to **Integrations** → menu (⋮) → **Custom repositories**.
3. Add:
   - **Repository URL**: `https://github.com/BigPappy098/n8n_conversation_agent`
   - **Category**: `Integration`
4. Search for **n8n Conversation Agent** in HACS and install.
5. **Restart Home Assistant**.

### 🔹 Manual
1. Download the latest release ZIP from the [Releases](../../releases) page.
2. Extract to:
   ```
   custom_components/n8n_conversation_agent/
   ```
3. **Restart Home Assistant**.

---

## ⚙️ Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **n8n Conversation Agent**.
3. Enter your **n8n Webhook URL** (e.g. `https://n8n.example.com/webhook/n8n_conversation_agent`).
4. Go to **Settings → Voice Assistants → Assist Pipelines** and select `n8n Conversation Agent` as your Conversation Agent.

---

## 🧪 Example n8n Workflow

Here’s a minimal example to confirm your setup works:

**Webhook Node**
- Method: `POST`
- Respond with: `Respond to Webhook` node

**Respond to Webhook Node**  
Send back:
```json
{
  "response": "Hello from n8n!"
}
```

When you speak to Assist, it should reply with “Hello from n8n!”.

---

## 🛠 Troubleshooting

- **Error:** `Unexpected error during intent recognition`  
  → Make sure your webhook returns valid JSON with a top-level `"response"` string.
- Enable debug logging in `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.n8n_conversation_agent: debug
```
- Check HA logs to see the raw n8n response.

---

## 📄 License

This project is licensed under the MIT License.

---

## ❤️ Contributing

PRs and feature requests are welcome! If you build amazing n8n workflows for Assist, share them in the repo’s discussions.

---

**Enjoy full automation freedom — connect Home Assistant’s voice control to the entire n8n universe.**
