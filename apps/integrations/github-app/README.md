# JARVIS GitHub App

GitHub App integration for JARVIS cognitive assistant.

## Features

- Issue management
- PR analysis and suggestions
- Commit insights
- Code review assistance
- Automated task creation

## Setup

1. Create GitHub App
2. Configure permissions
3. Install to repository
4. Configure webhooks

## Webhooks

- `issues` - Create tasks from issues
- `pull_request` - Analyze PRs
- `push` - Track commits
- `issue_comment` - Respond to comments

## Installation

```bash
pip install -r requirements.txt
python src/app.py
```

## Configuration

```env
GITHUB_APP_ID=123456
GITHUB_PRIVATE_KEY_PATH=/path/to/key.pem
GITHUB_WEBHOOK_SECRET=your-secret
JARVIS_API_URL=http://localhost:8000
```

## Permissions Required

- Issues: Read & Write
- Pull Requests: Read & Write
- Contents: Read
- Metadata: Read
