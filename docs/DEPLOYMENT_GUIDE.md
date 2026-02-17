# JARVIS Deployment Guide

This guide provides comprehensive instructions for deploying the JARVIS cognitive assistant in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- OS: Linux (Ubuntu 20.04+), macOS 10.15+, or Windows 10+

**Recommended Requirements:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 20GB+ SSD
- OS: Linux (Ubuntu 22.04+)

### Software Dependencies

- Python 3.8+ (Python 3.11 recommended)
- Node.js 18+ (for frontend)
- Docker 20.10+ and Docker Compose 2.0+ (for containerized deployment)
- PostgreSQL 13+ (production database)
- Redis 6+ (caching)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. Set Up Frontend

```bash
cd apps/web
npm install
```

### 4. Configure Environment Variables

Create `.env` file in the project root:

```bash
# Core Settings
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=postgresql://jarvis:password@localhost:5432/jarvis_dev

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

### 5. Start Infrastructure Services

```bash
# Start PostgreSQL and Redis using Docker Compose
docker-compose up -d postgres redis
```

### 6. Run Database Migrations

```bash
# Run Alembic migrations
cd apps/api
alembic upgrade head

# JARVIS V1: Enable pgvector extension for semantic search
psql $DATABASE_URL -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Verify pgvector is installed
psql $DATABASE_URL -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

**Note**: The `vector` extension enables PostgreSQL to store and query vector embeddings for semantic search capabilities introduced in JARVIS V1.

### 7. Start the Backend API

```bash
# From project root
cd apps/api
uvicorn jarvis_api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### 8. Start the Frontend

```bash
# In a new terminal
cd apps/web
npm run dev
```

The frontend will be available at http://localhost:5173

## Docker Deployment

### Development with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- API: http://localhost:8000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Production Docker Deployment

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale api=3
```

## Production Deployment

### Option 1: Direct Server Deployment

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv nginx postgresql redis-server

# Create application user
sudo useradd -m -s /bin/bash jarvis
sudo su - jarvis
```

#### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis

# Set up Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -e .

# Build frontend
cd apps/web
npm install
npm run build
```

#### 3. Configure Systemd Service

Create `/etc/systemd/system/jarvis-api.service`:

```ini
[Unit]
Description=JARVIS API Service
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=jarvis
WorkingDirectory=/home/jarvis/jarvis/apps/api
Environment="PATH=/home/jarvis/jarvis/venv/bin"
EnvironmentFile=/home/jarvis/jarvis/.env
ExecStart=/home/jarvis/jarvis/venv/bin/uvicorn jarvis_api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable jarvis-api
sudo systemctl start jarvis-api
sudo systemctl status jarvis-api
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/jarvis`:

```nginx
upstream jarvis_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name jarvis.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name jarvis.example.com;

    ssl_certificate /etc/letsencrypt/live/jarvis.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jarvis.example.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend
    root /home/jarvis/jarvis/apps/web/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://jarvis_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files
    location /static/ {
        alias /home/jarvis/jarvis/apps/api/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/jarvis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d jarvis.example.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Option 2: Kubernetes Deployment

#### 1. Create Kubernetes Manifests

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jarvis-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jarvis-api
  template:
    metadata:
      labels:
        app: jarvis-api
    spec:
      containers:
      - name: api
        image: jarvis/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: jarvis-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: jarvis-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 2. Apply Kubernetes Resources

```bash
# Create namespace
kubectl create namespace jarvis

# Apply configurations
kubectl apply -f k8s/ -n jarvis

# Check deployment
kubectl get pods -n jarvis
kubectl logs -f deployment/jarvis-api -n jarvis
```

## Environment Configuration

### Production Environment Variables

```bash
# Core Settings
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<strong-random-key>

# Database (use connection pooling)
DATABASE_URL=postgresql://user:password@db-host:5432/jarvis_prod?pool_size=20&max_overflow=0

# Redis (use sentinel for HA)
REDIS_URL=redis://redis-sentinel:26379/0

# OpenAI API
OPENAI_API_KEY=<your-production-key>

# JWT (use strong keys)
JWT_SECRET_KEY=<strong-random-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WORKERS=4

# Security
CORS_ORIGINS=https://jarvis.example.com
ALLOWED_HOSTS=jarvis.example.com

# JARVIS V1 - REFLECTOR Agent Configuration
REFLECTOR_ENABLED=true
REFLECTOR_ANALYSIS_SCHEDULE="0 6 * * *"  # Daily at 6 AM
REFLECTOR_MIN_TASKS_FOR_ANALYSIS=3

# JARVIS V1 - Semantic Search & ML/NLU Services
SEMANTIC_SEARCH_ENABLED=true
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSION=1536
VECTOR_SIMILARITY_THRESHOLD=0.7

# JARVIS V1 - Integration Services (Optional)
# GitHub App
GITHUB_APP_ID=<your-github-app-id>
GITHUB_PRIVATE_KEY_PATH=/path/to/github-private-key.pem
GITHUB_WEBHOOK_SECRET=<your-webhook-secret>

# Slack Bot
SLACK_BOT_TOKEN=xoxb-<your-bot-token>
SLACK_SIGNING_SECRET=<your-signing-secret>
SLACK_APP_TOKEN=xapp-<your-app-token>

# Monitoring
SENTRY_DSN=<your-sentry-dsn>
LOG_LEVEL=INFO
```

### Generate Strong Keys

```python
import secrets

# Generate SECRET_KEY
print(secrets.token_urlsafe(32))

# Generate JWT_SECRET_KEY
print(secrets.token_urlsafe(32))
```

## Monitoring and Maintenance

### Health Checks

```bash
# API health
curl https://jarvis.example.com/health

# Database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# Redis connectivity
redis-cli -u $REDIS_URL ping
```

### Logging

```bash
# View API logs
sudo journalctl -u jarvis-api -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View application logs
tail -f /home/jarvis/jarvis/logs/app.log
```

### Database Backups

```bash
# Create backup script
cat > /home/jarvis/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/jarvis/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
pg_dump $DATABASE_URL > $BACKUP_DIR/jarvis_$DATE.sql
gzip $BACKUP_DIR/jarvis_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "jarvis_*.sql.gz" -mtime +30 -delete
EOF

chmod +x /home/jarvis/backup.sh

# Schedule with cron
crontab -e
# Add: 0 2 * * * /home/jarvis/backup.sh
```

### Performance Monitoring

```bash
# Install monitoring tools
pip install prometheus-client
pip install py-spy

# Monitor with htop
htop

# Profile application
py-spy top --pid $(pgrep -f uvicorn)
```

## Troubleshooting

### Common Issues

#### 1. API Not Starting

```bash
# Check logs
sudo journalctl -u jarvis-api -n 100

# Check port availability
sudo netstat -tulpn | grep 8000

# Test configuration
source venv/bin/activate
python -c "from jarvis_api.main import app; print('OK')"
```

#### 2. Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT version();"

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### 3. Frontend Build Failures

```bash
# Clear cache and rebuild
cd apps/web
rm -rf node_modules dist
npm install
npm run build
```

#### 4. High Memory Usage

```bash
# Check memory usage
free -h

# Identify memory-intensive processes
ps aux --sort=-%mem | head -10

# Restart services
sudo systemctl restart jarvis-api
```

### Performance Optimization

#### Database Optimization

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM memories WHERE type = 'strategic';

-- Create indexes
CREATE INDEX idx_memories_type ON memories(type);
CREATE INDEX idx_tasks_status ON tasks(status);

-- Vacuum database
VACUUM ANALYZE;
```

#### Redis Optimization

```bash
# Monitor Redis
redis-cli --stat

# Check memory usage
redis-cli INFO memory

# Set max memory policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

## Security Checklist

- [ ] Use HTTPS with valid SSL certificates
- [ ] Change all default passwords and keys
- [ ] Enable firewall (ufw, firewalld)
- [ ] Configure rate limiting
- [ ] Enable database encryption at rest
- [ ] Regular security updates
- [ ] Implement backup strategy
- [ ] Set up monitoring and alerting
- [ ] Review and rotate API keys quarterly
- [ ] Enable audit logging

## Support

For deployment support:
- Documentation: https://docs.jarvis-ai.example.com
- GitHub Issues: https://github.com/lamiaakter14/jarvis/issues
- Email: support@jarvis-ai.example.com
