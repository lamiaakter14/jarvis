# Local Testing Guide

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Node.js 16+ installed
- [ ] Docker & Docker Compose installed
- [ ] Git installed

## Quick Start

```bash
# 1. Run quick start script
./scripts/setup/quick_start.sh

# 2. Edit .env with your API keys
nano .env

# 3. Start API (terminal 1)
make api

# 4. Start Web (terminal 2)
make web

# 5. Test CLI (terminal 3)
make cli ARGS="--help"
```

## Testing Each Component

### 1. Test API
```bash
# Start API
make api

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/cognitive-loop
curl http://localhost:8000/docs

# Expected: All endpoints respond successfully
```

### 2. Test Web Dashboard
```bash
# Start web
make web

# Open browser
open http://localhost:3000

# Expected: Dashboard loads, can navigate pages
```

### 3. Test CLI
```bash
# Run help command
make cli ARGS="--help"

# Run strategist
make cli ARGS="strategist plan"

# Run mentor
make cli ARGS="mentor gaps"

# Expected: Commands execute without errors
```

### 4. Test Database
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Run migrations
make db-migrate

# Seed test data (if seed script exists)
make seed

# Expected: No errors, data is seeded
```

### 5. Test Redis
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Expected: PONG
```

### 6. Run Tests
```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
make test-e2e

# Expected: Tests pass (or report existing failures)
```

### 7. Test Linting & Formatting
```bash
# Run linters
make lint

# Format code
make format

# Type check
make type-check

# Expected: Code passes linting checks
```

### 8. Test Docker
```bash
# Build images
make docker-build

# Start all services
make docker-up

# Check health
make health

# View logs
make docker-logs

# Stop services
make docker-down

# Expected: All services start and run
```

## Common Issues

### Issue: Port 8000 already in use
```bash
# Solution: Kill process or change port
lsof -ti:8000 | xargs kill -9
# Or edit .env and change API_PORT
```

### Issue: PostgreSQL connection failed
```bash
# Solution: Restart Docker services
docker-compose down
docker-compose up -d postgres
sleep 5
make db-migrate
```

### Issue: Node modules not found
```bash
# Solution: Reinstall dependencies
cd apps/web/dashboard
rm -rf node_modules package-lock.json
npm install
```

### Issue: Python module not found
```bash
# Solution: Reinstall Python dependencies
pip install -e .
```

### Issue: Permission denied on scripts
```bash
# Solution: Make scripts executable
chmod +x scripts/setup/quick_start.sh
```

## Testing Workflow

### Before Making Changes
1. Run `make clean` to clean artifacts
2. Run `make test` to ensure all tests pass
3. Run `make lint` to check code quality

### After Making Changes
1. Run `make format` to format code
2. Run `make test` to ensure tests still pass
3. Run `make lint` to verify code quality
4. Test the specific feature you changed

### Before Committing
1. Run `make clean` to remove artifacts
2. Run `make test` to ensure all tests pass
3. Run `make lint` to verify code quality
4. Manually test the changes

## Performance Testing

### API Load Testing
```bash
# Install hey (HTTP load testing tool)
go install github.com/rakyll/hey@latest

# Test API endpoint
hey -n 1000 -c 10 http://localhost:8000/health

# Expected: Low response time, no errors
```

### Memory Usage
```bash
# Check API memory usage
docker stats

# Expected: Reasonable memory consumption
```

## Security Testing

### Check for vulnerabilities
```bash
# Python dependencies
pip-audit

# Node dependencies
cd apps/web/dashboard
npm audit

# Expected: No critical vulnerabilities
```

## Integration Testing

### Full System Test
```bash
# 1. Start all services
docker-compose up -d

# 2. Run migrations
make db-migrate

# 3. Run integration tests
make test-integration

# 4. Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs

# 5. Test web dashboard
open http://localhost:3000

# Expected: All components work together
```

## Debugging Tips

### API Debugging
```bash
# Enable debug mode in .env
DEBUG=true

# Check API logs
tail -f runtime/logs/jarvis.log

# Check Docker logs
docker-compose logs -f api
```

### Database Debugging
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U jarvis

# List tables
\dt

# Query data
SELECT * FROM tasks LIMIT 10;
```

### Redis Debugging
```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check keys
KEYS *

# Get value
GET key_name
```

## Cleanup

### Clean temporary files
```bash
make clean
```

### Clean runtime data
```bash
make clean-runtime
```

### Reset database
```bash
make db-reset
# WARNING: This destroys all data!
```

### Stop all services
```bash
docker-compose down
```

### Remove all containers and volumes
```bash
docker-compose down -v
# WARNING: This removes all data!
```
