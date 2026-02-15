# JARVIS Production Deployment Checklist

## Pre-Deployment Checklist

### Infrastructure Readiness
- [ ] Run infrastructure verification script: `./scripts/deployment/verify_infrastructure.sh`
- [ ] All infrastructure checks pass
- [ ] Database is backed up
- [ ] SSL certificates are valid and up to date
- [ ] DNS records are configured correctly
- [ ] CDN/Load balancer is configured (if applicable)
- [ ] Firewall rules are configured
- [ ] Monitoring stack is running (Prometheus, Grafana, AlertManager)

### Code Readiness
- [ ] All tests pass on main branch
- [ ] Code review completed and approved
- [ ] Security scan passed (CodeQL, Bandit, Safety)
- [ ] No critical or high severity vulnerabilities
- [ ] Documentation is up to date
- [ ] CHANGELOG.md updated with release notes
- [ ] Version number bumped in pyproject.toml

### Configuration
- [ ] Production .env file configured with correct values
- [ ] All secrets rotated and stored securely
- [ ] API keys are valid and have proper permissions
- [ ] Database connection strings verified
- [ ] Redis connection string verified
- [ ] CORS origins configured for production domain
- [ ] Rate limiting configured appropriately
- [ ] Log levels set to INFO or WARNING

### Database
- [ ] Database migrations tested on staging
- [ ] Migration rollback plan documented
- [ ] Database backup completed within last 24 hours
- [ ] Database indexes optimized
- [ ] Database connection pool configured
- [ ] Database monitoring enabled

### Dependencies
- [ ] All Python dependencies installed and tested
- [ ] All npm dependencies installed and tested
- [ ] Dependency security audit passed
- [ ] No deprecated dependencies in use
- [ ] Pinned dependency versions in requirements

### Frontend
- [ ] Frontend built for production: `npm run build`
- [ ] Build artifacts verified
- [ ] Static assets optimized (minified, compressed)
- [ ] Environment variables configured correctly
- [ ] API endpoints point to production
- [ ] Source maps disabled or secured

### Security
- [ ] Security headers configured (X-Frame-Options, CSP, etc.)
- [ ] JWT secrets rotated and strong
- [ ] HTTPS enabled and enforced
- [ ] Authentication tested
- [ ] Rate limiting tested
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection enabled

### Monitoring & Alerting
- [ ] Prometheus scraping production endpoints
- [ ] Grafana dashboards configured
- [ ] Alert rules configured and tested
- [ ] AlertManager notification channels configured (Slack, PagerDuty)
- [ ] Log aggregation working (Loki/Promtail)
- [ ] Application performance monitoring configured
- [ ] Error tracking configured (Sentry or similar)

### Backup & Recovery
- [ ] Automated backup script tested
- [ ] Backup retention policy configured (30 days)
- [ ] Database backup tested and restorable
- [ ] File system backup tested and restorable
- [ ] Disaster recovery plan documented
- [ ] RPO (Recovery Point Objective) defined: 24 hours
- [ ] RTO (Recovery Time Objective) defined: 4 hours

### Documentation
- [ ] README.md updated
- [ ] API documentation current (Swagger/OpenAPI)
- [ ] Deployment guide reviewed and tested
- [ ] Architecture diagrams up to date
- [ ] Runbooks created for common issues
- [ ] Contact information updated

## Deployment Day Checklist

### Pre-Deployment (2-4 hours before)
- [ ] Announce maintenance window to users
- [ ] Create deployment ticket/issue
- [ ] Notify stakeholders of deployment start time
- [ ] Verify all pre-deployment checklist items
- [ ] Create fresh database backup
- [ ] Create code backup (git tag)
- [ ] Prepare rollback plan

### Deployment Window
- [ ] Put application in maintenance mode (if applicable)
- [ ] Stop API services: `docker-compose stop api`
- [ ] Pull latest code: `git pull origin main`
- [ ] Install dependencies: `pip install -e .`
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Build frontend: `cd apps/web && npm run build`
- [ ] Run smoke tests
- [ ] Start API services: `docker-compose up -d api`
- [ ] Remove maintenance mode

### Post-Deployment Verification (30 minutes)
- [ ] Health check endpoint responding: `/api/v1/health`
- [ ] All critical API endpoints tested
- [ ] Frontend loads correctly
- [ ] User authentication works
- [ ] Database queries executing properly
- [ ] Redis connectivity verified
- [ ] Logs show no errors
- [ ] Metrics being collected
- [ ] Response times within SLA (<500ms)
- [ ] No 5xx errors in logs

### Monitoring (1-2 hours)
- [ ] Watch error rates in Grafana
- [ ] Monitor response times
- [ ] Check memory and CPU usage
- [ ] Review application logs for errors
- [ ] Verify all alerts are working
- [ ] Check user feedback channels
- [ ] Monitor database performance

## Post-Deployment Checklist

### Immediate (Day 1)
- [ ] Deployment completed successfully
- [ ] No critical issues reported
- [ ] Error rates within normal range
- [ ] Performance metrics within SLA
- [ ] User feedback collected
- [ ] Stakeholders notified of completion
- [ ] Deployment notes documented

### Short-term (Week 1)
- [ ] Monitor user adoption of new features
- [ ] Address any minor issues
- [ ] Review performance trends
- [ ] Optimize slow queries if needed
- [ ] Update documentation based on feedback
- [ ] Collect and analyze metrics
- [ ] Schedule post-mortem meeting

### Long-term (Month 1)
- [ ] Review overall system stability
- [ ] Analyze performance trends
- [ ] Plan capacity upgrades if needed
- [ ] Update disaster recovery plan
- [ ] Conduct security audit
- [ ] Review and update monitoring
- [ ] Plan next release

## Rollback Procedure

If critical issues are detected:

### Immediate Rollback (Critical Issues)
1. [ ] Stop API services: `docker-compose stop api`
2. [ ] Restore code: `git reset --hard <previous-commit>`
3. [ ] Rollback database: Restore from backup
4. [ ] Restore configuration files
5. [ ] Start services: `docker-compose up -d api`
6. [ ] Verify services are healthy
7. [ ] Notify stakeholders of rollback

### Partial Rollback (Non-Critical Issues)
1. [ ] Identify problematic component
2. [ ] Disable feature flag (if applicable)
3. [ ] Deploy hotfix if possible
4. [ ] Monitor for improvement
5. [ ] Schedule full rollback if needed

## Emergency Contacts

### On-Call Rotation
- **Primary**: [Name] - [Phone] - [Email]
- **Secondary**: [Name] - [Phone] - [Email]
- **Manager**: [Name] - [Phone] - [Email]

### External Vendors
- **Cloud Provider**: [Support Link] - [Priority Ticket]
- **Database**: [Support Link] - [Priority Ticket]
- **CDN**: [Support Link] - [Priority Ticket]

## Success Criteria

Deployment is considered successful when:
- [ ] All services are running and healthy
- [ ] Error rate < 0.5%
- [ ] Response time p95 < 500ms
- [ ] No critical bugs reported
- [ ] All core features functional
- [ ] User satisfaction maintained
- [ ] 24 hours stable operation

## Sign-Off

### Deployment Team
- **DevOps Lead**: _________________ Date: _______
- **Backend Lead**: _________________ Date: _______
- **Frontend Lead**: _________________ Date: _______

### Management
- **Engineering Manager**: _________________ Date: _______
- **Product Owner**: _________________ Date: _______

### Notes
```
[Space for deployment notes, issues encountered, lessons learned]
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-15  
**Template for**: Production Deployment
