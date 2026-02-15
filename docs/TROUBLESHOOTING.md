# JARVIS Troubleshooting Guide

## Overview

This guide provides solutions to common issues you might encounter when using JARVIS. Issues are organized by category for easy navigation.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [API Issues](#api-issues)
3. [Database Issues](#database-issues)
4. [Frontend Issues](#frontend-issues)
5. [Docker Issues](#docker-issues)
6. [Performance Issues](#performance-issues)
7. [Authentication Issues](#authentication-issues)
8. [Integration Issues](#integration-issues)
9. [Deployment Issues](#deployment-issues)
10. [Monitoring Issues](#monitoring-issues)

---

## Installation Issues

### Python Version Issues

**Problem**: Wrong Python version or Python not found

**Symptoms**:
- `python: command not found`
- `This package requires Python >=3.9`
- Syntax errors due to old Python

**Solutions**:
```bash
# Check Python version
python --version
python3 --version
python3.11 --version

# Use specific Python version
python3.11 -m venv venv

# Add to PATH (Linux/macOS)
export PATH="/usr/local/bin/python3.11:$PATH"

# On Ubuntu, install Python 3.11
sudo apt install python3.11 python3.11-venv
```

---

### Dependency Installation Failures

**Problem**: pip install fails

**Symptoms**:
- `ERROR: Could not build wheels`
- `error: command 'gcc' failed`
- `Failed building wheel for psycopg2`

**Solutions**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install build dependencies (Ubuntu/Debian)
sudo apt install python3-dev libpq-dev build-essential

# Install build dependencies (macOS)
brew install postgresql

# Use binary packages
pip install psycopg2-binary  # Instead of psycopg2

# Clear pip cache and retry
pip cache purge
pip install -e ".[dev]"
```

---

### Virtual Environment Issues

**Problem**: Virtual environment not activating or commands not found

**Solutions**:
```bash
# Verify virtual environment exists
ls venv/bin/activate

# Create if missing
python3.11 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python  # Should show venv path
python --version  # Should show correct version

# If still issues, recreate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

---

## API Issues

### API Won't Start

**Problem**: API server fails to start

**Symptoms**:
- `ModuleNotFoundError`
- `ImportError`
- Port already in use

**Solutions**:
```bash
# 1. Check if module is installed
pip list | grep jarvis

# 2. Install if missing
pip install -e .

# 3. Check for port conflicts
sudo lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# 4. Kill conflicting process
kill -9 <PID>

# 5. Use different port
cd apps/api
uvicorn jarvis_api.main:app --port 8001

# 6. Check environment variables
cat ../../.env | grep -E "(DATABASE_URL|REDIS_URL|OPENAI_API_KEY)"

# 7. Check logs
tail -f ../../logs/api/error.log
```

---

### API Returns 500 Internal Server Error

**Problem**: API requests fail with 500 error

**Symptoms**:
- All endpoints return 500
- "Internal Server Error" message
- No specific error details

**Diagnosis**:
```bash
# Check API logs
docker logs jarvis-api --tail=100  # If using Docker
tail -f logs/api/error.log  # If running directly

# Test with verbose output
curl -v http://localhost:8000/api/v1/health

# Check database connection
psql -U jarvis -d jarvis_dev -c "SELECT 1;"

# Check Redis connection
redis-cli ping
```

**Common Causes & Solutions**:

1. **Database connection failed**:
```bash
# Verify DATABASE_URL in .env
grep DATABASE_URL .env

# Test connection
psql $DATABASE_URL -c "SELECT version();"

# Restart database
sudo systemctl restart postgresql
```

2. **Redis connection failed**:
```bash
# Verify REDIS_URL in .env
grep REDIS_URL .env

# Test connection
redis-cli -u $REDIS_URL ping

# Restart Redis
sudo systemctl restart redis-server
```

3. **Missing environment variables**:
```bash
# Check all required variables
grep -E "(DATABASE_URL|REDIS_URL|OPENAI_API_KEY|JWT_SECRET_KEY)" .env

# Set missing variables
export OPENAI_API_KEY="your-key-here"
```

---

### API Slow Response Times

**Problem**: API requests take too long

**Symptoms**:
- Requests timeout
- High latency (>2 seconds)
- Slow dashboard loading

**Diagnosis**:
```bash
# Measure response time
time curl http://localhost:8000/api/v1/health

# Check with verbose timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/tasks

# curl-format.txt:
# time_total: %{time_total}s
```

**Solutions**:

1. **Check database performance**:
```sql
-- Find slow queries
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Add missing indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_memories_type ON memories(type);

-- Analyze tables
VACUUM ANALYZE;
```

2. **Check Redis performance**:
```bash
# Monitor Redis
redis-cli --stat

# Check slow operations
redis-cli SLOWLOG GET 10

# Check memory
redis-cli INFO memory
```

3. **Optimize application**:
```python
# Enable query result caching
# Use async operations
# Implement pagination
# Reduce data returned
```

4. **Scale resources**:
```bash
# Increase API workers
uvicorn jarvis_api.main:app --workers 4

# Allocate more resources (Docker)
docker-compose up -d --scale api=3
```

---

## Database Issues

### Cannot Connect to Database

**Problem**: Database connection fails

**Symptoms**:
- `psycopg2.OperationalError: could not connect`
- `FATAL: password authentication failed`
- `Connection refused`

**Solutions**:

1. **Check if PostgreSQL is running**:
```bash
# Linux
sudo systemctl status postgresql
sudo systemctl start postgresql

# macOS
brew services list
brew services start postgresql

# Check if listening on port
sudo netstat -tulpn | grep 5432
```

2. **Verify credentials**:
```bash
# Test connection
psql -U jarvis -d jarvis_dev -h localhost -W

# If fails, reset password
sudo -u postgres psql
ALTER USER jarvis WITH PASSWORD 'new_password';
\q

# Update .env
DATABASE_URL=postgresql://jarvis:new_password@localhost:5432/jarvis_dev
```

3. **Check PostgreSQL configuration**:
```bash
# Edit postgresql.conf
sudo nano /etc/postgresql/13/main/postgresql.conf

# Ensure:
listen_addresses = 'localhost'
port = 5432

# Edit pg_hba.conf
sudo nano /etc/postgresql/13/main/pg_hba.conf

# Add/verify:
local   all             jarvis                                  md5
host    all             jarvis          127.0.0.1/32            md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

### Migration Failures

**Problem**: Alembic migrations fail

**Symptoms**:
- `Target database is not up to date`
- `Can't locate revision identified by`
- `FAILED: ... already exists`

**Solutions**:

1. **Check current migration**:
```bash
cd apps/api
alembic current
alembic history
```

2. **Reset migrations (WARNING: loses data)**:
```bash
# Downgrade to base
alembic downgrade base

# Upgrade to head
alembic upgrade head
```

3. **Force migration to specific revision**:
```bash
# Stamp to specific revision
alembic stamp head

# Then upgrade
alembic upgrade head
```

4. **Fresh database setup**:
```bash
# Drop and recreate database
dropdb jarvis_dev -U postgres
createdb jarvis_dev -U postgres -O jarvis

# Run migrations
alembic upgrade head
```

---

### Database Performance Issues

**Problem**: Slow database queries

**Solutions**:

1. **Identify slow queries**:
```sql
-- Enable logging
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- View slow queries
SELECT * FROM pg_stat_statements
WHERE mean_exec_time > 1000
ORDER BY mean_exec_time DESC;
```

2. **Add indexes**:
```sql
-- Find missing indexes
SELECT schemaname, tablename, attname
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100
  AND null_frac < 0.5;

-- Create indexes
CREATE INDEX CONCURRENTLY idx_tasks_status_priority 
ON tasks(status, priority);
```

3. **Optimize queries**:
```sql
-- Use EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM tasks WHERE status = 'pending';

-- Optimize with proper WHERE clauses
-- Use joins instead of subqueries
-- Limit result sets with LIMIT
```

4. **Regular maintenance**:
```sql
-- Vacuum and analyze
VACUUM ANALYZE tasks;
VACUUM ANALYZE memories;

-- Reindex
REINDEX TABLE tasks;
```

---

## Frontend Issues

### Frontend Won't Build

**Problem**: npm build fails

**Symptoms**:
- Build errors
- TypeScript errors
- Module not found

**Solutions**:

1. **Clean and rebuild**:
```bash
cd apps/web

# Remove old files
rm -rf node_modules dist package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall
npm install

# Build
npm run build
```

2. **Fix TypeScript errors**:
```bash
# Check for errors
npm run type-check

# Fix with auto-fix
npm run type-check -- --fix

# Update types
npm update @types/react @types/node
```

3. **Check Node.js version**:
```bash
node --version  # Should be 18+

# Use nvm to switch versions
nvm install 18
nvm use 18
```

---

### Frontend Shows Blank Page

**Problem**: Dashboard loads but shows nothing

**Symptoms**:
- White/blank screen
- Console shows errors
- React errors

**Solutions**:

1. **Check browser console**:
```javascript
// Open DevTools (F12)
// Look for errors in Console tab

// Common errors:
// - API connection errors
// - CORS errors
// - JavaScript errors
```

2. **Verify API connection**:
```bash
# Check if API is running
curl http://localhost:8000/api/v1/health

# Check CORS configuration
grep CORS_ORIGINS .env

# Should include frontend URL
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

3. **Clear browser cache**:
```
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete
- Safari: Cmd+Opt+E
```

4. **Check environment variables**:
```bash
# In apps/web/.env
VITE_API_URL=http://localhost:8000/api/v1

# Restart dev server
npm run dev
```

---

### CORS Errors

**Problem**: CORS policy blocks requests

**Symptoms**:
- `Access-Control-Allow-Origin` errors
- Network requests fail from browser
- OPTIONS preflight errors

**Solutions**:

1. **Update CORS origins**:
```bash
# Edit .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000

# Restart API
# Changes take effect immediately
```

2. **Check API configuration**:
```python
# In apps/api/jarvis_api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Temporary workaround** (development only):
```bash
# Run Chrome with disabled security (NOT for production)
chrome --disable-web-security --user-data-dir=/tmp/chrome
```

---

## Docker Issues

### Docker Build Fails

**Problem**: docker-compose build fails

**Solutions**:

1. **Clear Docker cache**:
```bash
# Remove old images
docker system prune -af

# Rebuild without cache
docker-compose build --no-cache
```

2. **Check Dockerfile syntax**:
```bash
# Validate Dockerfile
docker build -f Dockerfile --target=builder -t test .
```

3. **Check disk space**:
```bash
df -h
docker system df

# Clean up
docker system prune -a --volumes
```

---

### Docker Container Exits Immediately

**Problem**: Container starts then stops

**Solutions**:

1. **Check logs**:
```bash
# View container logs
docker logs jarvis-api

# Follow logs in real-time
docker logs -f jarvis-api
```

2. **Check environment variables**:
```bash
# Inspect container
docker inspect jarvis-api | jq '.[0].Config.Env'

# Verify .env file exists
ls -la .env
```

3. **Run interactively**:
```bash
# Start container with bash
docker-compose run --rm api bash

# Debug inside container
python -c "from jarvis_api.main import app; print('OK')"
```

---

### Docker Network Issues

**Problem**: Containers can't communicate

**Solutions**:

1. **Check network**:
```bash
# List networks
docker network ls

# Inspect network
docker network inspect jarvis_default

# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

2. **Use service names**:
```bash
# In .env, use service names
DATABASE_URL=postgresql://jarvis:password@postgres:5432/jarvis_dev
REDIS_URL=redis://redis:6379/0
```

---

## Performance Issues

### High CPU Usage

**Problem**: CPU usage constantly high

**Solutions**:

1. **Identify process**:
```bash
# Top processes
top
htop

# Docker stats
docker stats
```

2. **Profile application**:
```bash
# Use py-spy
pip install py-spy
py-spy top --pid $(pgrep -f uvicorn)
```

3. **Optimize code**:
- Use async operations
- Implement caching
- Reduce database queries
- Use connection pooling

---

### High Memory Usage

**Problem**: Memory usage grows over time

**Solutions**:

1. **Check for memory leaks**:
```bash
# Monitor memory
watch -n 1 'free -h'

# Check Docker memory
docker stats --no-stream
```

2. **Limit Docker memory**:
```yaml
# In docker-compose.yml
services:
  api:
    mem_limit: 2g
    mem_reservation: 1g
```

3. **Database cleanup**:
```sql
VACUUM FULL;
REINDEX DATABASE jarvis_dev;
```

4. **Redis cleanup**:
```bash
redis-cli FLUSHDB  # WARNING: Clears cache
```

---

## Authentication Issues

### JWT Token Invalid

**Problem**: Token validation fails

**Symptoms**:
- `401 Unauthorized`
- `Invalid token`
- `Token expired`

**Solutions**:

1. **Check token expiration**:
```bash
# Decode JWT (without verification)
python -c "
import jwt
token = 'your-token-here'
print(jwt.decode(token, options={'verify_signature': False}))
"
```

2. **Verify JWT secret**:
```bash
# Check .env
grep JWT_SECRET_KEY .env

# Ensure it matches between environments
```

3. **Clear old tokens**:
```bash
# Clear Redis tokens
redis-cli KEYS "token:*" | xargs redis-cli DEL
```

---

### Cannot Login

**Problem**: Login fails with correct credentials

**Solutions**:

1. **Check user exists**:
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

2. **Reset password**:
```python
# In Python shell
from jarvis_core.infrastructure.security import hash_password
hashed = hash_password("new_password")
print(hashed)

# Then in SQL:
UPDATE users SET password_hash = 'hashed_password' WHERE email = 'user@example.com';
```

3. **Check authentication logs**:
```bash
grep "authentication" logs/api/access.log
```

---

## Integration Issues

### OpenAI API Errors

**Problem**: OpenAI API calls fail

**Symptoms**:
- `Authentication error`
- `Rate limit exceeded`
- `Invalid API key`

**Solutions**:

1. **Verify API key**:
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

2. **Check rate limits**:
```bash
# View rate limit headers
curl -I https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

3. **Implement retry logic**:
```python
import time
from openai import RateLimitError

def call_openai_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if i < max_retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                raise
```

---

## Deployment Issues

### Deployment Fails

**Problem**: Production deployment fails

**Solutions**:

1. **Check prerequisites**:
```bash
./scripts/deployment/verify_infrastructure.sh
```

2. **Review deployment logs**:
```bash
tail -f /var/log/jarvis/deployment-*.log
```

3. **Rollback if needed**:
```bash
./scripts/deployment/deploy_production.sh --rollback
```

---

### Service Won't Start After Deployment

**Problem**: Service fails to start after deployment

**Solutions**:

1. **Check systemd status**:
```bash
sudo systemctl status jarvis-api
sudo journalctl -u jarvis-api -n 100
```

2. **Verify environment**:
```bash
# Check .env file
sudo -u jarvis cat /home/jarvis/jarvis/.env
```

3. **Test manually**:
```bash
# Run as jarvis user
sudo -u jarvis bash
cd /home/jarvis/jarvis
source venv/bin/activate
cd apps/api
uvicorn jarvis_api.main:app --host 0.0.0.0 --port 8000
```

---

## Monitoring Issues

### Prometheus Not Scraping

**Problem**: Prometheus can't collect metrics

**Solutions**:

1. **Check targets**:
```bash
# Visit Prometheus UI
open http://localhost:9090/targets

# Check status of each target
```

2. **Verify metrics endpoint**:
```bash
curl http://localhost:8000/metrics
```

3. **Check Prometheus config**:
```bash
# Validate config
docker exec jarvis-prometheus promtool check config /etc/prometheus/prometheus.yml

# Reload config
docker exec jarvis-prometheus killall -HUP prometheus
```

---

### Grafana Shows No Data

**Problem**: Grafana dashboards are empty

**Solutions**:

1. **Check data source**:
- Grafana → Configuration → Data Sources
- Test connection to Prometheus

2. **Verify queries**:
```promql
# Test in Prometheus UI
up{job="jarvis-api"}
rate(http_requests_total[5m])
```

3. **Check time range**:
- Ensure time range includes when data was collected
- Try "Last 5 minutes" to see recent data

---

## Getting Additional Help

### Reporting Issues

When reporting issues, include:

1. **Environment**:
```bash
# System info
uname -a
python --version
node --version
docker --version
```

2. **Error logs**:
```bash
# Recent logs
tail -n 100 logs/api/error.log
docker logs jarvis-api --tail=100
```

3. **Configuration** (sanitized):
```bash
# .env without secrets
grep -v -E "(API_KEY|SECRET|PASSWORD)" .env
```

4. **Steps to reproduce**

5. **Expected vs actual behavior**

### Support Channels

- **GitHub Issues**: https://github.com/lamiaakter14/jarvis/issues
- **Documentation**: https://github.com/lamiaakter14/jarvis/tree/main/docs
- **Discussions**: https://github.com/lamiaakter14/jarvis/discussions

---

**Document Version**: 1.0  
**Last Updated**: February 15, 2026  
**Contributors**: JARVIS Development Team
