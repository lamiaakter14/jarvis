# JARVIS Monitoring and Observability Guide

## Table of Contents

1. [Overview](#overview)
2. [Monitoring Stack](#monitoring-stack)
3. [Health Checks](#health-checks)
4. [Metrics Collection](#metrics-collection)
5. [Log Aggregation](#log-aggregation)
6. [Alerting Rules](#alerting-rules)
7. [Performance Monitoring](#performance-monitoring)
8. [Dashboard Setup](#dashboard-setup)
9. [Troubleshooting](#troubleshooting)

## Overview

This guide provides comprehensive instructions for monitoring the JARVIS system in production, including metrics collection, log aggregation, alerting, and performance monitoring.

**Monitoring Goals**:
- Detect issues before users report them
- Track system health and performance trends
- Provide visibility into system behavior
- Enable data-driven optimization decisions
- Ensure SLA compliance

## Monitoring Stack

### Core Components

```
Monitoring Architecture
├── Prometheus (Metrics Collection)
├── Grafana (Visualization)
├── Loki (Log Aggregation)
├── AlertManager (Alerting)
├── Node Exporter (System Metrics)
└── Custom Exporters (Application Metrics)
```

### Setup with Docker Compose

Add to your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: jarvis-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./infrastructure/monitoring/alerting/rules.yml:/etc/prometheus/rules.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    restart: always

  grafana:
    image: grafana/grafana:latest
    container_name: jarvis-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./infrastructure/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./infrastructure/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    restart: always

  loki:
    image: grafana/loki:latest
    container_name: jarvis-loki
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
      - ./infrastructure/monitoring/loki/loki-config.yml:/etc/loki/local-config.yaml
    command: -config.file=/etc/loki/local-config.yaml
    restart: always

  promtail:
    image: grafana/promtail:latest
    container_name: jarvis-promtail
    volumes:
      - /var/log:/var/log
      - ./infrastructure/monitoring/promtail/promtail-config.yml:/etc/promtail/config.yml
      - ./logs:/app/logs
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki
    restart: always

  node-exporter:
    image: prom/node-exporter:latest
    container_name: jarvis-node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: always

  alertmanager:
    image: prom/alertmanager:latest
    container_name: jarvis-alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./infrastructure/monitoring/alertmanager/config.yml:/etc/alertmanager/config.yml
      - alertmanager-data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/config.yml'
      - '--storage.path=/alertmanager'
    restart: always

volumes:
  prometheus-data:
  grafana-data:
  loki-data:
  alertmanager-data:
```

## Health Checks

### API Health Endpoint

The JARVIS API provides a comprehensive health check endpoint:

```python
GET /api/v1/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-15T21:00:00Z",
  "components": {
    "database": "healthy",
    "redis": "healthy",
    "ai_service": "healthy"
  },
  "metrics": {
    "uptime_seconds": 86400,
    "total_requests": 12500,
    "error_rate": 0.02,
    "avg_response_time_ms": 245
  }
}
```

### Enhanced Health Check Implementation

Update `apps/api/jarvis_api/src/api/v1/endpoints/health.py`:

```python
from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict
import asyncio
import psutil
from ...schemas.response import HealthResponse
from ...config.settings import settings
from ...db.session import get_db
from ...services.redis_client import get_redis

router = APIRouter()

async def check_database(db) -> str:
    """Check database connectivity."""
    try:
        await db.execute("SELECT 1")
        return "healthy"
    except Exception:
        return "unhealthy"

async def check_redis(redis) -> str:
    """Check Redis connectivity."""
    try:
        await redis.ping()
        return "healthy"
    except Exception:
        return "unhealthy"

@router.get("/health", response_model=HealthResponse)
async def health_check(
    db = Depends(get_db),
    redis = Depends(get_redis)
):
    """Comprehensive health check endpoint."""
    
    # Check all components
    db_status = await check_database(db)
    redis_status = await check_redis(redis)
    
    # Determine overall status
    overall_status = "healthy"
    if db_status != "healthy" or redis_status != "healthy":
        overall_status = "degraded"
    
    return {
        "status": overall_status,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
            "redis": redis_status,
            "ai_service": "healthy"  # Add AI service check
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    }

@router.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe - is the app running?"""
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness_probe(
    db = Depends(get_db),
    redis = Depends(get_redis)
):
    """Kubernetes readiness probe - can the app serve traffic?"""
    db_status = await check_database(db)
    redis_status = await check_redis(redis)
    
    if db_status == "healthy" and redis_status == "healthy":
        return {"status": "ready"}
    else:
        return {"status": "not_ready", "components": {
            "database": db_status,
            "redis": redis_status
        }}, 503
```

### Health Check Monitoring

Set up Prometheus to monitor health endpoints:

```yaml
# In prometheus.yml
scrape_configs:
  - job_name: 'jarvis-health'
    metrics_path: '/api/v1/health'
    scrape_interval: 30s
    static_configs:
      - targets: ['jarvis-api:8000']
```

## Metrics Collection

### Application Metrics

Add Prometheus client to your FastAPI application:

```python
# apps/api/jarvis_api/src/middleware/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently in progress'
)

# Task metrics
tasks_created_total = Counter(
    'tasks_created_total',
    'Total tasks created',
    ['priority', 'agent_type']
)

tasks_completed_total = Counter(
    'tasks_completed_total',
    'Total tasks completed',
    ['priority', 'agent_type', 'status']
)

task_execution_duration_seconds = Histogram(
    'task_execution_duration_seconds',
    'Task execution duration in seconds',
    ['agent_type']
)

# Memory metrics
memory_operations_total = Counter(
    'memory_operations_total',
    'Total memory operations',
    ['operation', 'memory_type']
)

active_memories = Gauge(
    'active_memories',
    'Number of active memories',
    ['memory_type']
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip metrics endpoint to avoid recursion
        if request.url.path == "/metrics":
            return await call_next(request)
        
        # Increment in-progress requests
        http_requests_in_progress.inc()
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            return response
        finally:
            # Decrement in-progress requests
            http_requests_in_progress.dec()

# Metrics endpoint
from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()

@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

### Key Metrics to Monitor

**API Metrics**:
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active connections
- Request payload size

**Application Metrics**:
- Task creation/completion rate
- Agent utilization
- Memory operations
- Cache hit/miss ratio
- AI API calls and latency

**System Metrics**:
- CPU usage
- Memory usage
- Disk I/O
- Network traffic
- Open file descriptors

**Business Metrics**:
- Active users
- Daily/monthly active users
- Feature usage
- User retention
- API usage by client

## Log Aggregation

### Structured Logging

Use structured logging for better log analysis:

```python
# packages/jarvis_core/infrastructure/monitoring/structured_logger.py
import logging
import json
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        self.logger.addHandler(handler)
    
    def log(self, level: str, message: str, **kwargs):
        """Log with structured data."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        
        getattr(self.logger, level.lower())(json.dumps(log_data))
    
    def info(self, message: str, **kwargs):
        self.log("INFO", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log("ERROR", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log("WARNING", message, **kwargs)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)
```

### Log Levels

Use appropriate log levels:

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical messages for serious failures

### Loki Configuration

Create `infrastructure/monitoring/loki/loki-config.yml`:

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 168h

storage_config:
  boltdb:
    directory: /loki/index
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 336h
```

### Promtail Configuration

Create `infrastructure/monitoring/promtail/promtail-config.yml`:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: jarvis-api
    static_configs:
      - targets:
          - localhost
        labels:
          job: jarvis-api
          __path__: /app/logs/api/*.log

  - job_name: jarvis-system
    static_configs:
      - targets:
          - localhost
        labels:
          job: system
          __path__: /var/log/*.log
```

## Alerting Rules

### AlertManager Configuration

Create `infrastructure/monitoring/alertmanager/config.yml`:

```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'YOUR_SLACK_WEBHOOK_URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
    
    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#jarvis-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#jarvis-warnings'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']
```

### Enhanced Alert Rules

Update `infrastructure/monitoring/alerting/rules.yml`:

```yaml
groups:
  - name: jarvis_critical_alerts
    interval: 30s
    rules:
      - alert: APIDown
        expr: up{job="jarvis-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "JARVIS API is down"
          description: "API has been down for more than 1 minute"
      
      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "PostgreSQL has been down for more than 2 minutes"
      
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 5% (current: {{ $value | humanizePercentage }})"
      
      - alert: HighResponseTime
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High response time"
          description: "99th percentile response time is {{ $value | humanizeDuration }} (threshold: 1s)"
      
      - alert: OutOfMemory
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.95
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "System out of memory"
          description: "Memory usage is {{ $value | humanizePercentage }} (threshold: 95%)"

  - name: jarvis_warning_alerts
    interval: 1m
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value | humanize }}% (threshold: 80%)"
      
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanizePercentage }} (threshold: 85%)"
      
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow response time"
          description: "95th percentile response time is {{ $value | humanizeDuration }} (threshold: 500ms)"
      
      - alert: HighDiskUsage
        expr: (node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High disk usage"
          description: "Disk usage is {{ $value | humanizePercentage }} (threshold: 85%)"
      
      - alert: LowCacheHitRate
        expr: rate(cache_hits_total[5m]) / rate(cache_requests_total[5m]) < 0.80
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Low cache hit rate"
          description: "Cache hit rate is {{ $value | humanizePercentage }} (threshold: 80%)"
```

## Performance Monitoring

### Response Time Tracking

Monitor API response times:

```bash
# Check current response times
curl -w "@curl-format.txt" -o /dev/null -s https://jarvis.example.com/api/v1/health

# Create curl-format.txt:
time_namelookup:  %{time_namelookup}\n
time_connect:     %{time_connect}\n
time_appconnect:  %{time_appconnect}\n
time_pretransfer: %{time_pretransfer}\n
time_redirect:    %{time_redirect}\n
time_starttransfer: %{time_starttransfer}\n
                  ----------\n
time_total:       %{time_total}\n
```

### Database Query Performance

Monitor slow queries:

```sql
-- Enable slow query logging in PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries > 1 second
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';
SELECT pg_reload_conf();

-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Redis Performance

Monitor Redis:

```bash
# Redis stats
redis-cli INFO stats

# Monitor commands in real-time
redis-cli MONITOR

# Check slow log
redis-cli SLOWLOG GET 10
```

## Dashboard Setup

### Grafana Dashboards

Create dashboards for different stakeholders:

**1. Operations Dashboard** (`infrastructure/monitoring/grafana/dashboards/operations.json`):
- Service uptime
- Error rates
- Response times
- System resources (CPU, memory, disk)
- Alert status

**2. Application Dashboard**:
- Task metrics (created, completed, failed)
- Agent activity and utilization
- Memory operations
- API usage statistics
- User activity

**3. Business Dashboard**:
- Active users
- Feature adoption
- User engagement
- API client usage
- Revenue metrics (if applicable)

### Sample Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "JARVIS Operations Dashboard",
    "panels": [
      {
        "title": "API Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Monitoring Issues

**1. Prometheus not scraping targets**:
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Prometheus config
docker exec jarvis-prometheus promtool check config /etc/prometheus/prometheus.yml

# Restart Prometheus
docker restart jarvis-prometheus
```

**2. Grafana not showing data**:
- Verify data source configuration
- Check Prometheus connectivity
- Verify query syntax
- Check time range selection

**3. Alerts not firing**:
```bash
# Check AlertManager status
curl http://localhost:9093/api/v1/status

# Check alert rules
docker exec jarvis-prometheus promtool check rules /etc/prometheus/rules.yml

# View active alerts
curl http://localhost:9090/api/v1/alerts
```

### Log Analysis

Query logs with LogQL (Loki query language):

```logql
# Search for errors
{job="jarvis-api"} |= "ERROR"

# Count errors by endpoint
sum by (endpoint) (rate({job="jarvis-api"} |= "ERROR" [5m]))

# Search for slow requests
{job="jarvis-api"} | json | duration > 1000

# Find authentication failures
{job="jarvis-api"} |= "authentication" |= "failed"
```

## Best Practices

1. **Set Appropriate Retention**: Keep metrics for 15-30 days, logs for 7-14 days
2. **Use Sampling**: Sample high-volume metrics to reduce storage
3. **Alert on Symptoms**: Alert on user-facing issues, not causes
4. **Reduce Alert Fatigue**: Tune thresholds to reduce false positives
5. **Document Runbooks**: Create runbooks for common alerts
6. **Regular Reviews**: Review dashboards and alerts quarterly
7. **Capacity Planning**: Monitor trends for capacity planning
8. **Test Alerts**: Regularly test alert delivery

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-15  
**Next Review**: Quarterly
