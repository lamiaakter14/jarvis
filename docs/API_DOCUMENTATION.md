# JARVIS API Documentation

## Overview

The JARVIS API provides a comprehensive set of endpoints for interacting with the AI-powered cognitive assistant. The API follows RESTful principles and supports both HTTP and WebSocket connections for real-time updates.

## Base URL

```
Production: https://jarvis-api.example.com/api/v1
Development: http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Obtaining a Token

```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Refreshing a Token

```http
POST /auth/refresh
Authorization: Bearer <your_refresh_token>
```

## Rate Limiting

- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

Rate limit information is included in response headers:
- `X-RateLimit-Limit-Minute`: Maximum requests per minute
- `X-RateLimit-Remaining-Minute`: Remaining requests in current minute
- `X-RateLimit-Limit-Hour`: Maximum requests per hour
- `X-RateLimit-Remaining-Hour`: Remaining requests in current hour

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "architecture": "clean_architecture",
  "agents": ["strategist", "mentor", "executor", "innovator", "amplifier", "reflector"]
}
```

### Cognitive Loop

#### POST /cognitive-loop/execute

Execute the complete cognitive loop with all 5 agents.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "strategist": {
    "plan": {...}
  },
  "mentor": {
    "gaps": [...],
    "task_feedback": [...]
  },
  "executor": {
    "status": "completed"
  },
  "innovator": {
    "innovations": [...]
  },
  "amplifier": {
    "performance": {...}
  },
  "reflector": {
    "reflection_summary": "...",
    "correction_actions": [...],
    "drift_analysis": {...}
  }
}
```

### Strategic Memory

#### POST /memory/strategic/goals

Create a strategic goal.

**Request Body:**
```json
{
  "goal": "Complete JARVIS final implementation",
  "description": "Finish all remaining tasks",
  "priority": "high",
  "target_date": "2024-12-31",
  "milestones": [
    {
      "title": "Memory Management",
      "completed": true
    }
  ],
  "metrics": {
    "test_coverage": 51
  }
}
```

**Response:**
```json
{
  "memory_id": "mem_abc123",
  "key": "strategic/goal_abc123",
  "status": "created"
}
```

#### GET /memory/strategic/goals

List all active strategic goals.

**Query Parameters:**
- `status`: Filter by status (active, paused, completed, cancelled)
- `priority`: Filter by priority (low, medium, high, critical)
- `limit`: Maximum number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "goals": [
    {
      "goal": "Complete JARVIS final implementation",
      "priority": "high",
      "status": "active",
      "progress": 75.0,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### PUT /memory/strategic/goals/{goal_id}/progress

Update goal progress.

**Request Body:**
```json
{
  "progress": 85.0,
  "notes": "Backend enhancements completed"
}
```

#### POST /memory/strategic/adrs

Create an Architecture Decision Record.

**Request Body:**
```json
{
  "title": "Use Clean Architecture",
  "context": "Need maintainable and testable codebase structure",
  "decision": "Implement clean architecture with domain-driven design",
  "consequences": "Improved maintainability, testability, and scalability",
  "alternatives": [
    "Monolithic architecture",
    "Microservices architecture"
  ],
  "status": "accepted"
}
```

### Tasks

#### GET /tasks

List tasks with optional filtering.

**Query Parameters:**
- `status`: Filter by status (pending, in_progress, completed, failed)
- `priority`: Filter by priority (low, medium, high, critical)
- `agent_type`: Filter by agent type
- `limit`: Maximum results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "tasks": [
    {
      "task_id": "task_123",
      "title": "Implement JWT authentication",
      "status": "completed",
      "priority": "high",
      "agent_type": "executor",
      "created_at": "2024-01-01T00:00:00Z",
      "completed_at": "2024-01-02T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### POST /tasks

Create a new task.

**Request Body:**
```json
{
  "title": "Add dark mode to dashboard",
  "description": "Implement dark mode toggle with persistence",
  "priority": "medium",
  "agent_type": "executor",
  "estimated_hours": 4.0
}
```

#### GET /tasks/{task_id}

Get task details.

**Response:**
```json
{
  "task_id": "task_123",
  "title": "Implement JWT authentication",
  "description": "Add JWT-based authentication to all API endpoints",
  "status": "completed",
  "priority": "high",
  "agent_type": "executor",
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-02T00:00:00Z",
  "result": {
    "status": "success",
    "files_modified": 5
  }
}
```

### Reflector Agent

#### POST /agents/reflector/analyze

Trigger REFLECTOR agent to analyze execution and suggest corrections.

**Request Body:**
```json
{
  "date": "2024-01-01",
  "context_id": "ctx_abc123"
}
```

**Response:**
```json
{
  "reflection_summary": "# Daily Reflection - 2024-01-01\n\n## Execution Performance\n- Tasks Completed: 8 / 10\n- Completion Rate: 80.0%\n- Strategic Alignment: 62.5%\n- Missed Tasks: 2\n\n## Drift Analysis\n- Drift Level: MINOR\n- Drift Score: 0.15\n\n## Recommended Corrections\n1. **Increase strategic task focus** (Priority 1)\n   Strategic alignment is 62.5%. Prioritize tasks that directly contribute to strategic goals.\n2. **Clear backlog of missed tasks** (Priority 2)\n   There are 2 missed tasks. Review and either reschedule, delegate, or cancel.\n3. **Review and optimize daily planning process** (Priority 3)\n   Analyze task estimation accuracy and planning effectiveness.",
  "correction_actions": [
    {
      "priority": 1,
      "action_type": "strategic_focus",
      "title": "Increase strategic task focus",
      "description": "Strategic alignment is 62.5%. Prioritize tasks that directly contribute to strategic goals.",
      "expected_impact": "high",
      "effort": "medium"
    },
    {
      "priority": 2,
      "action_type": "task_cleanup",
      "title": "Clear backlog of missed tasks",
      "description": "There are 2 missed tasks. Review and either reschedule, delegate, or cancel.",
      "expected_impact": "medium",
      "effort": "medium"
    },
    {
      "priority": 3,
      "action_type": "process_improvement",
      "title": "Review and optimize daily planning process",
      "description": "Analyze task estimation accuracy and planning effectiveness.",
      "expected_impact": "medium",
      "effort": "low"
    }
  ],
  "pattern_flags": [
    {
      "type": "strategic_misalignment",
      "severity": "high",
      "description": "Strategic alignment below target: 62.5%"
    }
  ],
  "skill_graph_updates": [
    {
      "skill_pattern": "strategic_planning",
      "suggested_weight": 0.9,
      "reason": "Low strategic alignment - boost strategic planning skills",
      "current_weight": 0.5
    }
  ],
  "drift_analysis": {
    "drift_score": 0.15,
    "drift_level": "minor",
    "requires_intervention": false
  }
}
```

#### GET /agents/reflector/history

Get historical reflection data.

**Query Parameters:**
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)
- `limit`: Maximum results (default: 30)

**Response:**
```json
{
  "reflections": [
    {
      "date": "2024-01-01",
      "drift_level": "minor",
      "drift_score": 0.15,
      "completion_rate": 0.8,
      "strategic_alignment": 0.625,
      "corrections_count": 3
    }
  ],
  "total": 1
}
```

### Integration Endpoints

#### POST /integrations/github/webhook

Handle GitHub webhook events (for GitHub App integration).

**Headers:**
```
X-GitHub-Event: push
X-Hub-Signature-256: sha256=...
```

**Request Body:** GitHub webhook payload (varies by event type)

**Response:**
```json
{
  "status": "processed",
  "event_type": "push",
  "actions_taken": [
    "created_task_for_new_issue",
    "updated_memory_with_code_changes"
  ]
}
```

#### POST /integrations/slack/command

Handle Slack slash commands.

**Request Body:**
```json
{
  "command": "/jarvis",
  "text": "status",
  "user_id": "U123ABC",
  "channel_id": "C456DEF"
}
```

**Response:**
```json
{
  "response_type": "in_channel",
  "text": "JARVIS Status: Healthy\n• Tasks: 8 completed, 5 pending\n• Strategic alignment: 87.5%\n• Last cognitive loop: 2 hours ago"
}
```

#### GET /integrations/vscode/context

Get context data for VSCode extension.

**Query Parameters:**
- `file_path`: Current file path
- `project_root`: Project root directory

**Response:**
```json
{
  "relevant_tasks": [
    {
      "task_id": "task_123",
      "title": "Implement authentication",
      "status": "in_progress",
      "file_path": "src/auth.py"
    }
  ],
  "knowledge_snippets": [
    {
      "key": "auth_best_practices",
      "content": "Use JWT tokens with refresh mechanism",
      "relevance_score": 0.92
    }
  ],
  "suggestions": [
    "Consider implementing rate limiting for auth endpoints"
  ]
}
```

### Analytics

#### GET /analytics/dashboard

Get comprehensive analytics data.

**Query Parameters:**
- `timeRange`: Time range for analytics (24h, 7d, 30d)

**Response:**
```json
{
  "taskProgress": [
    {
      "date": "2024-01-01",
      "completed": 45,
      "pending": 12,
      "failed": 2
    }
  ],
  "memoryUsage": [
    {
      "type": "Knowledge",
      "count": 128,
      "size": 15.7
    }
  ],
  "performanceMetrics": [
    {
      "timestamp": "2024-01-01T00:00:00Z",
      "latency": 245,
      "throughput": 1250
    }
  ],
  "agentActivity": [
    {
      "agent": "Executor",
      "tasks": 342,
      "successRate": 94
    }
  ]
}
```

### Agent Coordination

#### POST /agents/coordinate

Coordinate task execution across agents.

**Request Body:**
```json
{
  "priority_threshold": "medium",
  "max_concurrent": 3
}
```

**Response:**
```json
{
  "total_tasks": 15,
  "executed": 12,
  "failed": 1,
  "skipped": 2,
  "duration_seconds": 45.2
}
```

#### POST /agents/synchronize

Synchronize STRATEGIST, EXECUTOR, and MENTOR agents.

**Response:**
```json
{
  "workflow": "strategic_agents_sync",
  "overall_status": "success",
  "steps": [
    {
      "step": "strategy",
      "agent": "STRATEGIST",
      "status": "success",
      "result": {...}
    },
    {
      "step": "execution",
      "agent": "EXECUTOR",
      "status": "success",
      "result": {...}
    },
    {
      "step": "mentoring",
      "agent": "MENTOR",
      "status": "success",
      "result": {...}
    }
  ]
}
```

## WebSocket API

### Connection

Connect to the WebSocket endpoint for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/cognitive-loop');

ws.onopen = () => {
  console.log('Connected to JARVIS');
  // Authenticate after connection
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'your_jwt_token'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
  handleEvent(data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from JARVIS');
  // Implement reconnection logic
};
```

### Real-time Event Types

#### Cognitive Loop Progress

Receive real-time updates during cognitive loop execution:

```json
{
  "type": "cognitive_loop_progress",
  "stage": "strategist",
  "status": "in_progress",
  "progress": 25,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Task Status Updates

```json
{
  "type": "task_update",
  "task_id": "task_123",
  "status": "completed",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Agent Execution Updates

```json
{
  "type": "agent_update",
  "agent": "EXECUTOR",
  "status": "executing",
  "task_id": "task_123",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Memory Updates

```json
{
  "type": "memory_update",
  "memory_type": "strategic",
  "action": "created",
  "key": "strategic/goal_abc123",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Reflector Analysis Updates

```json
{
  "type": "reflector_analysis",
  "date": "2024-01-01",
  "drift_level": "minor",
  "drift_score": 0.15,
  "corrections_available": 3,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": {
    "field": "priority",
    "issue": "must be one of: low, medium, high, critical"
  }
}
```

### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden

```json
{
  "error": "Forbidden",
  "message": "Admin privileges required"
}
```

### 429 Too Many Requests

```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 60 requests per minute allowed",
  "retry_after": 60
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "detail": "Error details for debugging"
}
```

## Best Practices

### 1. Always Use HTTPS in Production

Never send authentication tokens over unencrypted connections in production.

### 2. Handle Rate Limiting

Implement exponential backoff when receiving 429 responses:

```python
import time

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)
```

### 3. Use WebSockets for Real-Time Updates

For applications requiring real-time updates, use WebSocket connections instead of polling.

### 4. Implement Token Refresh

Refresh tokens before they expire to maintain seamless user experience:

```javascript
async function refreshTokenIfNeeded() {
  const expiresAt = localStorage.getItem('token_expires_at');
  const now = Date.now();
  
  if (now >= expiresAt - 300000) { // Refresh 5 minutes before expiry
    await refreshToken();
  }
}
```

### 5. Validate Input Data

Always validate and sanitize input data before sending to the API.

## SDK Examples

### Python

```python
from jarvis_client import JarvisClient

client = JarvisClient(
    base_url="https://jarvis-api.example.com",
    api_key="your_api_key"
)

# Create strategic goal
goal = client.strategic_memory.create_goal(
    goal="Complete project",
    priority="high",
    description="Finish all tasks"
)

# List tasks
tasks = client.tasks.list(status="pending", priority="high")

# Execute cognitive loop
result = client.cognitive_loop.execute()
```

### JavaScript/TypeScript

```typescript
import { JarvisClient } from '@jarvis/client';

const client = new JarvisClient({
  baseUrl: 'https://jarvis-api.example.com',
  apiKey: 'your_api_key'
});

// Create strategic goal
const goal = await client.strategicMemory.createGoal({
  goal: 'Complete project',
  priority: 'high',
  description: 'Finish all tasks'
});

// List tasks
const tasks = await client.tasks.list({
  status: 'pending',
  priority: 'high'
});

// Execute cognitive loop
const result = await client.cognitiveLoop.execute();
```

## Support

For API support, please contact:
- Email: support@jarvis-ai.example.com
- Documentation: https://docs.jarvis-ai.example.com
- GitHub Issues: https://github.com/lamiaakter14/jarvis/issues
