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
  "agents": ["strategist", "mentor", "executor", "innovator", "amplifier"]
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

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to JARVIS');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Events

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
