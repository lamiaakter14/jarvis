# JARVIS Project Handover Document

## Executive Summary

This document provides comprehensive information for the operations and maintenance team taking over the JARVIS AI-Powered Cognitive Assistant system. It includes system architecture, operational procedures, troubleshooting guides, and contact information.

**Project**: JARVIS - AI-Powered Cognitive Assistant  
**Version**: 1.0.0  
**Handover Date**: February 15, 2026  
**Status**: Production Ready  

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Infrastructure](#infrastructure)
4. [Operational Procedures](#operational-procedures)
5. [Monitoring & Alerting](#monitoring--alerting)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance Schedule](#maintenance-schedule)
8. [Security & Compliance](#security--compliance)
9. [Documentation](#documentation)
10. [Contacts & Escalation](#contacts--escalation)

## System Overview

### Purpose
JARVIS is an enterprise-grade AI cognitive assistant that leverages multi-agent architecture to help users with strategic planning, task execution, innovation, and performance optimization.

### Key Features
- Strategic memory management and goal tracking
- Multi-agent task coordination
- Real-time analytics dashboard
- RESTful API with JWT authentication
- Dark mode and user preferences
- Rate limiting and security headers
- Comprehensive monitoring and alerting

### Technology Stack

**Backend**:
- Python 3.9-3.11
- FastAPI (REST API)
- PostgreSQL 13+ (database)
- Redis 6+ (caching)
- Alembic (migrations)

**Frontend**:
- React 18
- TypeScript
- Vite (build tool)
- Tailwind CSS
- Recharts (analytics)

**Infrastructure**:
- Docker & Docker Compose
- Nginx (reverse proxy)
- Let's Encrypt (SSL)
- Prometheus (metrics)
- Grafana (dashboards)
- Loki (logs)

### SLA Targets
- **Availability**: 99.5% uptime (43.8 hours downtime/year allowed)
- **Response Time**: p95 < 500ms, p99 < 1s
- **Error Rate**: < 0.5%
- **Recovery Time Objective (RTO)**: 4 hours
- **Recovery Point Objective (RPO)**: 24 hours

## Architecture

### High-Level Architecture

```
                                    ┌─────────────┐
                                    │   Users     │
                                    └──────┬──────┘
                                           │
                                    ┌──────▼──────┐
                                    │  Nginx/SSL  │
                                    │  (Port 443) │
                                    └──────┬──────┘
                                           │
                  ┌────────────────────────┼────────────────────────┐
                  │                        │                        │
           ┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
           │   Web UI    │         │  REST API   │         │   WebSocket │
           │ (React/TS)  │         │  (FastAPI)  │         │   (Socket)  │
           │  Port 3000  │         │  Port 8000  │         │  Port 8001  │
           └─────────────┘         └──────┬──────┘         └─────────────┘
                                           │
                                  ┌────────┼────────┐
                                  │        │        │
                           ┌──────▼────┐  │  ┌─────▼─────┐
                           │ PostgreSQL │  │  │   Redis   │
                           │  Port 5432 │  │  │ Port 6379 │
                           └────────────┘  │  └───────────┘
                                           │
                                  ┌────────▼────────┐
                                  │ Agent Coordinator│
                                  │   (5 Agents)    │
                                  └─────────────────┘
```

### Component Details

**Web Frontend**:
- Location: `apps/web/`
- Build command: `npm run build`
- Deployment: Static files served by Nginx
- Port: 3000 (dev), 443 (prod via Nginx)

**API Backend**:
- Location: `apps/api/jarvis_api/`
- Start command: `uvicorn jarvis_api.main:app`
- Workers: 4 (production)
- Port: 8000

**Database**:
- PostgreSQL 13+
- Database name: `jarvis_prod`
- User: `jarvis`
- Port: 5432
- Backup: Daily at 2:00 AM

**Cache**:
- Redis 6+
- Configuration: Standalone
- Port: 6379
- Max memory: 2GB with LRU eviction

### Data Flow

1. **User Request**: HTTPS request → Nginx → API
2. **Authentication**: JWT validation → Redis cache lookup
3. **Business Logic**: API → Agent Coordinator → Agents
4. **Data Persistence**: API → PostgreSQL
5. **Caching**: API → Redis (frequently accessed data)
6. **Response**: API → Nginx → User

## Infrastructure

### Server Specifications

**Production Server**:
- **Hostname**: jarvis-prod-01
- **IP**: 10.0.1.10 (internal), 203.0.113.10 (public)
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 8 cores
- **RAM**: 16GB
- **Disk**: 100GB SSD
- **Location**: us-east-1

### Directory Structure

```
/home/jarvis/
├── jarvis/                    # Application code
│   ├── apps/                  # Applications
│   ├── packages/              # Core packages
│   ├── docs/                  # Documentation
│   ├── scripts/               # Operational scripts
│   ├── .env                   # Environment config
│   └── docker-compose.prod.yml
├── backups/                   # Database backups
│   ├── jarvis_YYYYMMDD_HHMMSS_db.sql.gz
│   └── jarvis_YYYYMMDD_HHMMSS_files.tar.gz
├── logs/                      # Application logs
│   ├── api/
│   ├── web/
│   └── deployment/
└── monitoring/                # Monitoring data
    ├── prometheus/
    └── grafana/
```

### Docker Containers

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| jarvis-api | jarvis/api:latest | 8000 | API server |
| jarvis-web | jarvis/web:latest | 3000 | Web frontend |
| jarvis-postgres | postgres:13 | 5432 | Database |
| jarvis-redis | redis:6 | 6379 | Cache |
| jarvis-prometheus | prom/prometheus | 9090 | Metrics |
| jarvis-grafana | grafana/grafana | 3001 | Dashboards |
| jarvis-loki | grafana/loki | 3100 | Logs |
| jarvis-alertmanager | prom/alertmanager | 9093 | Alerts |

### Network Configuration

- **Domain**: jarvis.example.com
- **SSL**: Let's Encrypt (auto-renewal enabled)
- **Firewall**: UFW enabled
  - 22/tcp (SSH, restricted)
  - 80/tcp (HTTP redirect)
  - 443/tcp (HTTPS)
  - 9090/tcp (Prometheus, internal only)
  - 3001/tcp (Grafana, internal only)

## Operational Procedures

### Daily Operations

**Morning Checks** (9:00 AM):
1. Check Grafana dashboards for overnight issues
2. Review error logs: `tail -f /home/jarvis/logs/api/error.log`
3. Verify backup completion: `ls -lh /home/jarvis/backups/`
4. Check disk space: `df -h`
5. Review alerts: Check Slack #jarvis-alerts channel

**Evening Checks** (6:00 PM):
1. Review day's metrics in Grafana
2. Check for any warning alerts
3. Verify all services running: `docker-compose ps`

### Weekly Operations

**Monday**:
- Review week's deployment schedule
- Check for security updates
- Review user feedback

**Wednesday**:
- Performance review (response times, error rates)
- Database performance analysis
- Check for slow queries

**Friday**:
- Weekly backup verification (restore test)
- Review monitoring dashboards
- Update runbooks if needed
- Plan next week's maintenance

### Service Management

**Start Services**:
```bash
cd /home/jarvis/jarvis
docker-compose -f docker-compose.prod.yml up -d
```

**Stop Services**:
```bash
cd /home/jarvis/jarvis
docker-compose -f docker-compose.prod.yml down
```

**Restart Single Service**:
```bash
docker-compose -f docker-compose.prod.yml restart api
```

**View Logs**:
```bash
# Real-time logs
docker-compose -f docker-compose.prod.yml logs -f api

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 api
```

**Health Check**:
```bash
curl https://jarvis.example.com/api/v1/health | jq
```

### Backup & Recovery

**Manual Backup**:
```bash
# Create backup
sudo -u jarvis /home/jarvis/backup.sh

# Verify backup
ls -lh /home/jarvis/backups/ | tail -5
```

**Restore from Backup**:
```bash
# Stop services
docker-compose -f docker-compose.prod.yml stop

# Restore database
gunzip -c /home/jarvis/backups/jarvis_YYYYMMDD_HHMMSS_db.sql.gz | \
  docker exec -i jarvis-postgres psql -U jarvis jarvis_prod

# Restore files
cd /home/jarvis
tar -xzf backups/jarvis_YYYYMMDD_HHMMSS_files.tar.gz

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Verify
curl https://jarvis.example.com/api/v1/health
```

**Automated Backups**:
- Schedule: Daily at 2:00 AM
- Retention: 30 days
- Location: `/home/jarvis/backups/`
- Cron: `0 2 * * * /home/jarvis/backup.sh`

### Deployment Process

**Standard Deployment** (requires 30-60 minutes):
```bash
# 1. Verify infrastructure
cd /home/jarvis/jarvis
./scripts/deployment/verify_infrastructure.sh

# 2. Create backup
./scripts/deployment/deploy_production.sh
# (Script handles backup, deployment, and verification)

# 3. Monitor for 1 hour
# Watch Grafana, check logs, verify health
```

**Emergency Hotfix**:
```bash
# 1. Pull hotfix
git fetch origin
git checkout hotfix/critical-fix

# 2. Quick deploy (skip tests for speed)
docker-compose -f docker-compose.prod.yml restart api

# 3. Verify fix
curl https://jarvis.example.com/api/v1/health
```

**Rollback**:
```bash
# Rollback using deployment script
cd /home/jarvis/jarvis
# Script automatically uses latest backup for rollback
./scripts/deployment/deploy_production.sh --rollback

# Manual rollback
git reset --hard <previous-commit>
docker-compose -f docker-compose.prod.yml restart api
```

## Monitoring & Alerting

### Grafana Dashboards

Access: https://jarvis.example.com:3001  
Credentials: admin / [stored in 1Password]

**Main Dashboards**:
1. **Operations Overview**: System health, uptime, resource usage
2. **API Performance**: Response times, error rates, throughput
3. **Application Metrics**: Tasks, agents, memory operations
4. **Database Performance**: Query times, connections, cache hits
5. **Business Metrics**: Users, feature usage, engagement

### Key Metrics

**Critical Metrics** (alert immediately):
- API availability < 99%
- Error rate > 1%
- Response time p99 > 2s
- Database down
- Redis down
- Disk usage > 90%

**Warning Metrics** (investigate within 1 hour):
- Error rate > 0.5%
- Response time p95 > 500ms
- CPU usage > 80%
- Memory usage > 85%
- Disk usage > 85%

### Alert Channels

**Critical Alerts**:
- PagerDuty (on-call rotation)
- Slack #jarvis-critical
- Email to ops-team@example.com

**Warning Alerts**:
- Slack #jarvis-alerts
- Email to dev-team@example.com

**Info Notifications**:
- Slack #jarvis-info

## Troubleshooting

### Common Issues

#### Issue: API Returns 502 Bad Gateway

**Symptoms**: Nginx returns 502, API container running

**Diagnosis**:
```bash
# Check API logs
docker logs jarvis-api --tail=50

# Check if API is responding
curl http://localhost:8000/api/v1/health
```

**Resolution**:
```bash
# Restart API container
docker-compose -f docker-compose.prod.yml restart api

# If persists, check database connectivity
docker exec jarvis-postgres pg_isready
```

**Prevention**: Ensure database and Redis are healthy before API starts

---

#### Issue: High Memory Usage

**Symptoms**: Memory alert, system slowness

**Diagnosis**:
```bash
# Check memory usage
free -h

# Check container memory
docker stats --no-stream

# Check for memory leaks
docker exec jarvis-api ps aux --sort=-%mem | head -10
```

**Resolution**:
```bash
# Restart high-memory containers
docker-compose -f docker-compose.prod.yml restart api

# If PostgreSQL is high:
docker exec jarvis-postgres psql -U jarvis -c "VACUUM ANALYZE;"

# If Redis is high:
docker exec jarvis-redis redis-cli FLUSHDB
```

**Prevention**: Regular database maintenance, cache expiration policies

---

#### Issue: Slow Response Times

**Symptoms**: Response time alert, user complaints

**Diagnosis**:
```bash
# Check Grafana for bottlenecks
# Check database slow queries
docker exec jarvis-postgres psql -U jarvis -d jarvis_prod -c \
  "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Check API logs for slow requests
grep "duration" /home/jarvis/logs/api/access.log | sort -k10 -n | tail
```

**Resolution**:
```bash
# Add indexes to slow queries
docker exec jarvis-postgres psql -U jarvis -d jarvis_prod -c \
  "CREATE INDEX idx_memories_type ON memories(type);"

# Restart services to clear any issues
docker-compose -f docker-compose.prod.yml restart
```

**Prevention**: Regular performance reviews, proactive indexing

---

#### Issue: Disk Space Full

**Symptoms**: Disk usage alert, write failures

**Diagnosis**:
```bash
# Check disk usage
df -h

# Find large files
du -sh /home/jarvis/* | sort -h | tail -10
```

**Resolution**:
```bash
# Clean old logs
find /home/jarvis/logs -type f -mtime +30 -delete

# Clean old backups
cd /home/jarvis/backups
ls -t | tail -n +31 | xargs rm

# Clean Docker
docker system prune -af --volumes
```

**Prevention**: Automated log rotation, backup retention policies

---

### Escalation Procedures

**Level 1 - Operations Team** (response within 1 hour):
- Service restart
- Log analysis
- Basic troubleshooting

**Level 2 - Development Team** (response within 4 hours):
- Code issues
- Performance optimization
- Bug fixes

**Level 3 - Management** (response within 24 hours):
- Strategic decisions
- Major incidents
- Customer escalations

## Maintenance Schedule

### Daily
- 2:00 AM: Automated database backup
- 3:00 AM: Log rotation
- 6:00 AM: Health checks

### Weekly
- Sunday 3:00 AM: Full system backup
- Wednesday 10:00 AM: Performance review meeting

### Monthly
- First Monday: Security updates
- Second Monday: Database optimization (VACUUM, ANALYZE)
- Third Monday: SSL certificate renewal check
- Fourth Monday: Capacity planning review

### Quarterly
- Security audit
- Disaster recovery drill
- Documentation review
- Training sessions

### Annually
- Infrastructure upgrade planning
- Renewal of SSL certificates
- Review and update SLAs
- Comprehensive security assessment

## Security & Compliance

### Access Control

**Production Server Access**:
- SSH access restricted to operations team
- SSH key authentication only (no passwords)
- Fail2ban enabled for brute force protection

**Database Access**:
- No direct external access
- Accessed only via API or authorized tools
- All queries logged

**API Access**:
- JWT authentication required
- Rate limiting: 60 req/min, 1000 req/hour
- API keys rotated quarterly

### Security Practices

**Secrets Management**:
- Environment variables stored securely
- Secrets rotated every 90 days
- No secrets in code or version control

**Updates**:
- Security patches applied within 7 days
- Regular dependency updates
- CVE monitoring enabled

**Monitoring**:
- Failed login attempts logged
- Unusual activity triggers alerts
- Quarterly security audits

### Compliance

- **Data Protection**: User data encrypted at rest and in transit
- **Audit Logging**: All critical operations logged
- **Backup Compliance**: Daily backups, 30-day retention
- **Incident Response**: Documented procedures

## Documentation

### Available Documentation

**User Documentation**:
- README.md - Getting started
- docs/QUICK_START.md - Quick start guide
- docs/USAGE_GUIDE.md - Comprehensive usage guide
- docs/API_DOCUMENTATION.md - API reference

**Operations Documentation**:
- docs/DEPLOYMENT_GUIDE.md - Deployment procedures
- docs/DEPLOYMENT_CHECKLIST.md - Deployment checklist
- docs/MONITORING_GUIDE.md - Monitoring setup
- docs/UAT_GUIDE.md - UAT procedures
- docs/HANDOVER.md - This document

**Architecture Documentation**:
- docs/architecture/ - Architecture diagrams and decisions
- docs/PROJECT_SUMMARY.md - Project overview

### Knowledge Base

**Wiki**: https://wiki.example.com/jarvis  
**Runbooks**: /home/jarvis/jarvis/docs/runbooks/  
**Postmortems**: /home/jarvis/jarvis/docs/postmortems/

## Contacts & Escalation

### Team Contacts

**Operations Team**:
- Lead: John Doe - john.doe@example.com - +1-555-0101
- Engineer: Jane Smith - jane.smith@example.com - +1-555-0102

**Development Team**:
- Lead: Bob Johnson - bob.johnson@example.com - +1-555-0201
- Backend: Alice Williams - alice.williams@example.com - +1-555-0202
- Frontend: Charlie Brown - charlie.brown@example.com - +1-555-0203

**Management**:
- Engineering Manager: David Lee - david.lee@example.com - +1-555-0301
- Product Owner: Emma Davis - emma.davis@example.com - +1-555-0302

### On-Call Rotation

**Week of Feb 15-21, 2026**:
- Primary: John Doe
- Secondary: Jane Smith

**Week of Feb 22-28, 2026**:
- Primary: Jane Smith
- Secondary: John Doe

### External Support

**Cloud Provider**: AWS Support - support.aws.amazon.com - Priority ticket
**Database**: PostgreSQL Community - stackoverflow.com/questions/tagged/postgresql
**SSL Certificates**: Let's Encrypt - https://letsencrypt.org/docs/

### Communication Channels

- **Slack**: #jarvis-ops, #jarvis-alerts, #jarvis-incidents
- **Email**: ops@example.com, support@example.com
- **Ticketing**: Jira project JARVIS
- **Status Page**: status.example.com/jarvis

## Appendices

### Appendix A: Service Level Agreements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.5% | Monthly |
| Response Time (p95) | < 500ms | 5-minute average |
| Response Time (p99) | < 1s | 5-minute average |
| Error Rate | < 0.5% | Daily average |
| Data Loss | 0% | Per incident |
| Recovery Time | < 4 hours | Per incident |

### Appendix B: Change Management

**Change Request Process**:
1. Submit change request in Jira
2. Risk assessment by operations team
3. Approval by engineering manager
4. Schedule maintenance window
5. Execute change following runbook
6. Post-change verification
7. Update documentation

**Emergency Changes**:
- May skip formal approval
- Must be documented post-incident
- Requires post-mortem review

### Appendix C: Incident Response

**Incident Severity Levels**:
- **P0 (Critical)**: Complete system outage, data loss
- **P1 (High)**: Major feature unavailable, severe performance degradation
- **P2 (Medium)**: Minor feature issue, workaround available
- **P3 (Low)**: Cosmetic issue, no user impact

**Response Times**:
- P0: Immediate (< 15 minutes)
- P1: < 1 hour
- P2: < 4 hours
- P3: Next business day

### Appendix D: Glossary

- **API**: Application Programming Interface
- **JWT**: JSON Web Token
- **SLA**: Service Level Agreement
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective
- **p95/p99**: 95th/99th percentile

---

**Document Version**: 1.0  
**Created**: February 15, 2026  
**Last Updated**: February 15, 2026  
**Next Review**: May 15, 2026  
**Owner**: Operations Team

---

## Sign-Off

**Developed By**: Development Team  
**Signature**: _________________ Date: _______

**Accepted By**: Operations Team  
**Signature**: _________________ Date: _______

**Approved By**: Engineering Manager  
**Signature**: _________________ Date: _______
