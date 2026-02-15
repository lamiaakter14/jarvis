#!/bin/bash

# JARVIS Infrastructure Readiness Verification Script
# Verifies all infrastructure components are ready for production deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

check_item() {
    local description=$1
    local command=$2
    
    echo -ne "${BLUE}[→]${NC} $description... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC}"
        ((FAILED++))
        return 1
    fi
}

warning_item() {
    local description=$1
    echo -e "${YELLOW}[!]${NC} $description"
    ((WARNINGS++))
}

section() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Main checks
echo "=========================================="
echo "JARVIS Infrastructure Readiness Check"
echo "Timestamp: $(date)"
echo "=========================================="

section "System Requirements"
check_item "CPU cores >= 4" "[ $(nproc) -ge 4 ]"
check_item "Memory >= 8GB" "[ $(free -g | awk 'NR==2 {print $2}') -ge 8 ]"
check_item "Disk space >= 20GB available" "[ $(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//') -ge 20 ]"
check_item "Operating system is Linux" "[ -f /etc/os-release ]"

section "Required Software"
check_item "Python 3.8+ installed" "command -v python3 && python3 --version | grep -qE '3\.(8|9|10|11|12)'"
check_item "Node.js 18+ installed" "command -v node && node --version | grep -qE 'v(1[8-9]|[2-9][0-9])'"
check_item "Docker 20.10+ installed" "command -v docker && docker --version | grep -qE '(2[0-9]|[3-9][0-9])'"
check_item "Docker Compose 2.0+ installed" "command -v docker-compose && docker-compose --version | grep -qE '(2\.[0-9]|v2\.[0-9])'"
check_item "Git installed" "command -v git"
check_item "Curl installed" "command -v curl"
check_item "jq installed" "command -v jq"

section "Docker Services"
check_item "Docker daemon is running" "docker info"
check_item "PostgreSQL container exists" "docker ps -a | grep -q jarvis-postgres"
check_item "PostgreSQL container is running" "docker ps | grep -q jarvis-postgres"
check_item "Redis container exists" "docker ps -a | grep -q jarvis-redis"
check_item "Redis container is running" "docker ps | grep -q jarvis-redis"

section "Database Connectivity"
check_item "PostgreSQL is accepting connections" "docker exec jarvis-postgres pg_isready -U jarvis"
check_item "Can connect to database" "docker exec jarvis-postgres psql -U jarvis -d jarvis_prod -c 'SELECT 1'"
check_item "Redis is accepting connections" "docker exec jarvis-redis redis-cli ping"

section "Network Connectivity"
check_item "Can reach Docker network" "docker network inspect jarvis_default"
check_item "Outbound internet connectivity" "curl -s --max-time 5 https://www.google.com"
check_item "Can resolve DNS" "nslookup google.com"

section "Application Files"
APP_DIR="/home/jarvis/jarvis"
check_item "Application directory exists" "[ -d $APP_DIR ]"
check_item "Git repository is valid" "cd $APP_DIR && git status"
check_item ".env file exists" "[ -f $APP_DIR/.env ]"
check_item "Python virtual environment exists" "[ -d $APP_DIR/venv ]"
check_item "Frontend build directory exists" "[ -d $APP_DIR/apps/web/dist ]" || warning_item "Frontend not built (run: npm run build)"

section "Environment Variables"
check_item "DATABASE_URL is set" "grep -q 'DATABASE_URL=' $APP_DIR/.env"
check_item "REDIS_URL is set" "grep -q 'REDIS_URL=' $APP_DIR/.env"
check_item "OPENAI_API_KEY is set" "grep -q 'OPENAI_API_KEY=' $APP_DIR/.env"
check_item "JWT_SECRET_KEY is set" "grep -q 'JWT_SECRET_KEY=' $APP_DIR/.env"
check_item "ENVIRONMENT is set to production" "grep -q 'ENVIRONMENT=production' $APP_DIR/.env" || warning_item "ENVIRONMENT not set to production"

section "SSL/TLS Configuration"
check_item "SSL certificate exists" "[ -f /etc/letsencrypt/live/jarvis.example.com/fullchain.pem ]" || warning_item "SSL certificate not found"
check_item "SSL private key exists" "[ -f /etc/letsencrypt/live/jarvis.example.com/privkey.pem ]" || warning_item "SSL private key not found"
check_item "Nginx is installed" "command -v nginx" || warning_item "Nginx not installed"
check_item "Nginx configuration exists" "[ -f /etc/nginx/sites-available/jarvis ]" || warning_item "Nginx configuration not found"

section "Monitoring Stack"
check_item "Prometheus container running" "docker ps | grep -q jarvis-prometheus" || warning_item "Prometheus not running"
check_item "Grafana container running" "docker ps | grep -q jarvis-grafana" || warning_item "Grafana not running"
check_item "AlertManager container running" "docker ps | grep -q jarvis-alertmanager" || warning_item "AlertManager not running"

section "Security"
check_item "Firewall is active" "command -v ufw && sudo ufw status | grep -q active" || warning_item "Firewall not configured"
check_item "SSH key authentication" "grep -q 'PasswordAuthentication no' /etc/ssh/sshd_config" || warning_item "SSH password authentication still enabled"
check_item "Fail2ban is installed" "command -v fail2ban-client" || warning_item "Fail2ban not installed"

section "Backup Configuration"
check_item "Backup directory exists" "[ -d /home/jarvis/backups ]"
check_item "Backup script exists" "[ -f /home/jarvis/backup.sh ]" || warning_item "Backup script not found"
check_item "Cron job for backups" "crontab -l | grep -q backup" || warning_item "Backup cron job not configured"

section "Resource Limits"
echo -e "${BLUE}[→]${NC} Current resource usage:"
echo "  CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')% used"
echo "  Memory: $(free -h | awk 'NR==2 {print $3 "/" $2}') used"
echo "  Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2}') used"

section "Application Health"
if docker ps | grep -q jarvis-api; then
    if curl -s --max-time 10 http://localhost:8000/api/v1/health | jq -e '.status == "healthy"' &>/dev/null; then
        echo -e "${GREEN}[✓]${NC} API health check passed"
        ((PASSED++))
    else
        echo -e "${RED}[✗]${NC} API health check failed"
        ((FAILED++))
    fi
else
    warning_item "API container not running"
fi

# Summary
echo ""
echo "=========================================="
echo -e "Readiness Check Complete"
echo ""
echo -e "Results:"
echo -e "  ${GREEN}Passed:${NC}   $PASSED"
echo -e "  ${RED}Failed:${NC}   $FAILED"
echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ System is ready for production deployment${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠ System is ready but has warnings. Review warnings before deployment.${NC}"
        exit 0
    fi
else
    echo -e "${RED}✗ System is NOT ready for production deployment${NC}"
    echo -e "Please fix the failed checks before deploying."
    exit 1
fi
