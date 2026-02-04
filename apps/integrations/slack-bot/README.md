# JARVIS Slack Bot

Slack integration for JARVIS cognitive assistant.

## Features

- Receive commands via Slack
- Post updates and notifications
- Interactive message buttons
- Slash commands

## Setup

1. Create a Slack App
2. Add bot permissions
3. Install to workspace
4. Configure environment variables

## Commands

- `/jarvis plan` - Get today's plan
- `/jarvis gaps` - Get knowledge gaps
- `/jarvis innovations` - Get innovations
- `/jarvis status` - Get system status

## Installation

```bash
pip install -r requirements.txt
python src/bot.py
```

## Configuration

```env
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
JARVIS_API_URL=http://localhost:8000
```
