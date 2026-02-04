# JARVIS API

Enterprise-grade FastAPI service for JARVIS cognitive assistant.

## Features

- **Versioned API**: v1 and v2 API endpoints
- **WebSocket Support**: Real-time updates for cognitive loop and events
- **Advanced Middleware**: 
  - JWT Authentication
  - Rate Limiting
  - Request Logging
  - CORS Configuration
  - Global Error Handling
- **Database Migrations**: Alembic integration
- **Comprehensive Schemas**: Pydantic models for validation
- **Clean Architecture**: Organized codebase with clear separation of concerns

## Directory Structure

```
jarvis_api/
├── src/
│   ├── api/
│   │   ├── v1/              # Version 1 API
│   │   │   ├── endpoints/   # REST endpoints
│   │   │   └── websocket/   # WebSocket endpoints
│   │   └── v2/              # Version 2 API (future)
│   ├── middleware/          # Middleware layers
│   ├── config/              # Configuration
│   ├── schemas/             # Pydantic schemas
│   ├── dependencies.py      # FastAPI dependencies
│   └── main.py              # Application entry point
├── tests/                   # Tests
├── alembic/                 # Database migrations
├── requirements/            # Environment-specific requirements
└── README.md
```

## API Endpoints

### Version 1 (v1)

#### REST Endpoints
- `GET /api/v1/health` - Health check
- `POST /api/v1/cognitive-loop` - Execute cognitive loop
- `GET /api/v1/plan/today` - Get daily plan
- `GET /api/v1/gaps` - Get knowledge gaps
- `GET /api/v1/innovations` - Get innovations
- `GET /api/v1/performance` - Get performance metrics

#### WebSocket Endpoints
- `WS /api/v1/ws/cognitive-loop/{client_id}` - Real-time cognitive loop updates
- `WS /api/v1/ws/events/{client_id}` - Real-time system events

## Installation

### Development
```bash
pip install -r requirements/dev.txt
```

### Production
```bash
pip install -r requirements/prod.txt
```

## Configuration

Create a `.env` file:

```env
APP_NAME="JARVIS Cognitive Assistant API"
APP_VERSION="1.0.0"
DEBUG=false
HOST=0.0.0.0
PORT=8000

DATABASE_URL=sqlite:///./jarvis.db
REDIS_URL=redis://localhost:6379/0

SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

RATE_LIMIT_PER_MINUTE=60
OPENAI_API_KEY=your-openai-key
```

## Running the API

### Development
```bash
python -m jarvis_api.src.main
```

### Production
```bash
gunicorn jarvis_api.src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Database Migrations

```bash
# Create a migration
alembic revision --autogenerate -m "Description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Testing

```bash
pytest tests/ -v --cov=jarvis_api
```

## WebSocket Usage

### JavaScript Example
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/cognitive-loop/client-123');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Start cognitive loop
ws.send(JSON.stringify({type: 'start_loop'}));
```

## Authentication

API uses JWT authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

## Rate Limiting

API enforces rate limiting: 60 requests per minute per IP address by default.

## License

See LICENSE file in repository root.
