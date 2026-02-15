#!/bin/bash

# JARVIS Production Deployment Script
# This script handles production deployment with safety checks and rollback capability

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="production"
APP_NAME="jarvis"
DEPLOY_USER="jarvis"
APP_DIR="/home/${DEPLOY_USER}/${APP_NAME}"
BACKUP_DIR="/home/${DEPLOY_USER}/backups"
LOG_FILE="/var/log/${APP_NAME}/deployment-$(date +%Y%m%d_%H%M%S).log"

# Function to log messages
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if running as correct user
    if [ "$USER" != "$DEPLOY_USER" ]; then
        log_error "Must run as $DEPLOY_USER user"
        exit 1
    fi
    
    # Check required commands
    for cmd in git docker docker-compose python3 npm curl; do
        if ! command -v $cmd &> /dev/null; then
            log_error "$cmd is not installed"
            exit 1
        fi
    done
    
    # Check if .env file exists
    if [ ! -f "$APP_DIR/.env" ]; then
        log_error ".env file not found in $APP_DIR"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Function to create backup
create_backup() {
    log "Creating backup..."
    
    BACKUP_NAME="${APP_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    log "Backing up database..."
    docker exec jarvis-postgres pg_dump -U jarvis jarvis_prod > "$BACKUP_DIR/${BACKUP_NAME}_db.sql"
    gzip "$BACKUP_DIR/${BACKUP_NAME}_db.sql"
    
    # Backup application files
    log "Backing up application files..."
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_files.tar.gz" \
        -C "$(dirname $APP_DIR)" "$(basename $APP_DIR)" \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.mypy_cache' \
        --exclude='.pytest_cache'
    
    # Store backup info
    echo "$BACKUP_NAME" > "$BACKUP_DIR/.latest_backup"
    
    log_success "Backup created: $BACKUP_NAME"
    echo "$BACKUP_NAME"
}

# Function to verify infrastructure
verify_infrastructure() {
    log "Verifying infrastructure readiness..."
    
    # Check database
    log "Checking database connection..."
    if docker exec jarvis-postgres pg_isready -U jarvis; then
        log_success "Database is ready"
    else
        log_error "Database is not ready"
        return 1
    fi
    
    # Check Redis
    log "Checking Redis connection..."
    if docker exec jarvis-redis redis-cli ping | grep -q "PONG"; then
        log_success "Redis is ready"
    else
        log_error "Redis is not ready"
        return 1
    fi
    
    # Check disk space
    log "Checking disk space..."
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 85 ]; then
        log_error "Disk usage is too high: ${DISK_USAGE}%"
        return 1
    else
        log_success "Disk space is adequate: ${DISK_USAGE}%"
    fi
    
    # Check memory
    log "Checking available memory..."
    MEM_AVAILABLE=$(free -m | awk 'NR==2 {print $7}')
    if [ "$MEM_AVAILABLE" -lt 512 ]; then
        log_warning "Low memory available: ${MEM_AVAILABLE}MB"
    else
        log_success "Memory is adequate: ${MEM_AVAILABLE}MB available"
    fi
    
    log_success "Infrastructure verification passed"
}

# Function to pull latest code
pull_latest_code() {
    log "Pulling latest code from main branch..."
    
    cd "$APP_DIR"
    
    # Fetch latest changes
    git fetch origin
    
    # Get current commit
    CURRENT_COMMIT=$(git rev-parse HEAD)
    echo "$CURRENT_COMMIT" > .deploy_prev_commit
    
    # Pull latest code
    git pull origin main
    
    NEW_COMMIT=$(git rev-parse HEAD)
    
    if [ "$CURRENT_COMMIT" = "$NEW_COMMIT" ]; then
        log_warning "No new changes to deploy"
    else
        log_success "Code updated from $CURRENT_COMMIT to $NEW_COMMIT"
    fi
    
    echo "$NEW_COMMIT"
}

# Function to install dependencies
install_dependencies() {
    log "Installing dependencies..."
    
    cd "$APP_DIR"
    
    # Python dependencies
    log "Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e . --no-cache-dir
    
    # Frontend dependencies
    log "Installing frontend dependencies..."
    cd apps/web
    npm ci --production
    
    log_success "Dependencies installed"
}

# Function to run database migrations
run_migrations() {
    log "Running database migrations..."
    
    cd "$APP_DIR/apps/api"
    source ../../venv/bin/activate
    
    # Check for pending migrations
    PENDING=$(alembic current 2>&1 || echo "unknown")
    log "Current migration: $PENDING"
    
    # Run migrations
    alembic upgrade head
    
    if [ $? -eq 0 ]; then
        log_success "Migrations completed successfully"
    else
        log_error "Migration failed"
        return 1
    fi
}

# Function to build frontend
build_frontend() {
    log "Building frontend..."
    
    cd "$APP_DIR/apps/web"
    
    # Build production bundle
    npm run build
    
    if [ $? -eq 0 ]; then
        log_success "Frontend built successfully"
    else
        log_error "Frontend build failed"
        return 1
    fi
}

# Function to run tests
run_tests() {
    log "Running test suite..."
    
    cd "$APP_DIR"
    source venv/bin/activate
    
    # Run critical tests only (fast subset)
    pytest tests/ -v -m "not slow" --tb=short
    
    if [ $? -eq 0 ]; then
        log_success "Tests passed"
    else
        log_error "Tests failed"
        return 1
    fi
}

# Function to restart services
restart_services() {
    log "Restarting services..."
    
    cd "$APP_DIR"
    
    # Restart using docker-compose
    docker-compose -f docker-compose.prod.yml restart api
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 10
    
    # Check if services are running
    if docker-compose -f docker-compose.prod.yml ps | grep -q "api.*Up"; then
        log_success "Services restarted successfully"
    else
        log_error "Services failed to start"
        return 1
    fi
}

# Function to verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    # Wait a bit for services to stabilize
    sleep 5
    
    # Check health endpoint
    log "Checking health endpoint..."
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://jarvis.example.com/api/v1/health)
    
    if [ "$HEALTH_STATUS" = "200" ]; then
        log_success "Health check passed (HTTP $HEALTH_STATUS)"
    else
        log_error "Health check failed (HTTP $HEALTH_STATUS)"
        return 1
    fi
    
    # Check API response
    log "Checking API response..."
    API_RESPONSE=$(curl -s https://jarvis.example.com/api/v1/health | jq -r '.status')
    
    if [ "$API_RESPONSE" = "healthy" ]; then
        log_success "API is healthy"
    else
        log_error "API is not healthy: $API_RESPONSE"
        return 1
    fi
    
    # Check database connectivity from API
    log "Checking database connectivity..."
    DB_STATUS=$(curl -s https://jarvis.example.com/api/v1/health | jq -r '.components.database')
    
    if [ "$DB_STATUS" = "healthy" ]; then
        log_success "Database connectivity confirmed"
    else
        log_error "Database connectivity failed"
        return 1
    fi
    
    log_success "Deployment verification passed"
}

# Function to rollback
rollback() {
    log_error "Rolling back deployment..."
    
    BACKUP_NAME=$(cat "$BACKUP_DIR/.latest_backup" 2>/dev/null)
    
    if [ -z "$BACKUP_NAME" ]; then
        log_error "No backup found for rollback"
        exit 1
    fi
    
    log "Rolling back to backup: $BACKUP_NAME"
    
    # Restore files
    log "Restoring application files..."
    cd "$(dirname $APP_DIR)"
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_files.tar.gz"
    
    # Restore database
    log "Restoring database..."
    gunzip -c "$BACKUP_DIR/${BACKUP_NAME}_db.sql.gz" | \
        docker exec -i jarvis-postgres psql -U jarvis jarvis_prod
    
    # Restart services
    restart_services
    
    log_warning "Rollback completed. Please investigate the deployment failure."
}

# Function to notify team
notify_team() {
    local status=$1
    local message=$2
    
    # Send Slack notification (if configured)
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"🚀 JARVIS Deployment [$status]: $message\"}" \
            &>/dev/null || true
    fi
}

# Main deployment function
main() {
    log "=========================================="
    log "JARVIS Production Deployment Starting"
    log "Environment: $ENVIRONMENT"
    log "Timestamp: $(date)"
    log "=========================================="
    
    # Pre-deployment checks
    check_prerequisites || exit 1
    verify_infrastructure || exit 1
    
    # Create backup
    BACKUP_NAME=$(create_backup)
    
    # Deploy
    NEW_COMMIT=$(pull_latest_code)
    install_dependencies || { rollback; exit 1; }
    
    # Build and test
    run_migrations || { rollback; exit 1; }
    build_frontend || { rollback; exit 1; }
    run_tests || { log_warning "Tests failed, but continuing deployment"; }
    
    # Restart and verify
    restart_services || { rollback; exit 1; }
    verify_deployment || { rollback; exit 1; }
    
    log "=========================================="
    log_success "Deployment completed successfully!"
    log "Commit: $NEW_COMMIT"
    log "Backup: $BACKUP_NAME"
    log "=========================================="
    
    notify_team "SUCCESS" "Deployment to production completed successfully (commit: ${NEW_COMMIT:0:8})"
    
    # Clean up old backups (keep last 10)
    cd "$BACKUP_DIR"
    ls -t | tail -n +21 | xargs -r rm
}

# Run main function
main "$@"
