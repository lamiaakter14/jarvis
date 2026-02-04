# JARVIS VS Code Extension

VS Code extension for JARVIS cognitive assistant.

## Features

- Quick access to JARVIS from VS Code
- Inline task management
- View cognitive loop status
- AI-powered code suggestions
- Command palette integration

## Installation

1. Open VS Code
2. Go to Extensions
3. Search for "JARVIS"
4. Click Install

Or install from VSIX:
```bash
code --install-extension jarvis-vscode-0.1.0.vsix
```

## Usage

- `Ctrl+Shift+J` - Open JARVIS panel
- `Cmd+K Cmd+J` - Quick command
- Right-click in editor - "Ask JARVIS"

## Configuration

```json
{
  "jarvis.apiUrl": "http://localhost:8000",
  "jarvis.apiKey": "your-api-key",
  "jarvis.enableAutoSuggestions": true
}
```

## Development

```bash
npm install
npm run compile
npm run watch
```
