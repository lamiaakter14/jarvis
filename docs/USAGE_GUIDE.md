# JARVIS Usage Guide

Welcome to JARVIS, your AI-powered cognitive assistant! This guide will help you get started and make the most of JARVIS's powerful features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Strategic Memory Management](#strategic-memory-management)
4. [Task Management](#task-management)
5. [Agent Coordination](#agent-coordination)
6. [Analytics and Insights](#analytics-and-insights)
7. [User Preferences](#user-preferences)
8. [Advanced Features](#advanced-features)
9. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### First-Time Setup

1. **Access JARVIS**: Navigate to your JARVIS instance (e.g., `https://jarvis.example.com`)

2. **Login**: Enter your credentials to access the dashboard

3. **Initial Configuration**: Set your preferences:
   - Choose your theme (Light, Dark, or System)
   - Set your preferred font size
   - Configure notification settings

### Quick Tour

JARVIS consists of five key components:

1. **Strategist**: Plans and prioritizes your tasks
2. **Executor**: Executes tasks efficiently
3. **Mentor**: Provides guidance and identifies gaps
4. **Innovator**: Generates creative solutions
5. **Amplifier**: Analyzes performance and suggests improvements

## Dashboard Overview

### Main Dashboard

The main dashboard provides an at-a-glance view of your system:

- **Task Summary**: Current tasks, completion rates, and priorities
- **Agent Activity**: Real-time status of all agents
- **Quick Actions**: Common operations accessible with one click
- **Recent Activities**: Latest updates and changes

### Navigation Menu

- **Dashboard**: Main overview
- **Tasks**: Task management interface
- **Strategic Memory**: Long-term goals and ADRs
- **Analytics**: Detailed performance metrics
- **Settings**: User preferences and configuration

## Strategic Memory Management

Strategic memory helps you maintain long-term context and make informed decisions.

### Creating Strategic Goals

1. Navigate to **Strategic Memory** → **Goals**
2. Click **New Goal**
3. Fill in the details:
   - **Goal**: Clear, concise description
   - **Priority**: Low, Medium, High, or Critical
   - **Description**: Detailed explanation
   - **Target Date**: Expected completion date
   - **Milestones**: Break down into smaller steps
   - **Metrics**: Define success criteria

Example:
```
Goal: Achieve 90% test coverage
Priority: High
Description: Improve codebase reliability through comprehensive testing
Target Date: 2024-12-31
Milestones:
  - Unit tests for core modules (60% coverage)
  - Integration tests (75% coverage)
  - E2E tests (90% coverage)
Metrics:
  - Test coverage percentage
  - Code quality score
```

### Tracking Progress

1. Open your goal from the goals list
2. Click **Update Progress**
3. Enter progress percentage and notes
4. Mark milestones as completed

The system automatically:
- Tracks historical progress
- Calculates completion velocity
- Suggests adjustments to timeline

### Architecture Decision Records (ADRs)

Document important architectural decisions:

1. Navigate to **Strategic Memory** → **ADRs**
2. Click **New ADR**
3. Fill in:
   - **Title**: Brief decision summary
   - **Context**: Why this decision is needed
   - **Decision**: What you decided to do
   - **Consequences**: Expected outcomes
   - **Alternatives**: Options you considered
   - **Status**: Proposed, Accepted, Deprecated, or Superseded

ADRs help maintain architectural consistency and provide context for future decisions.

## Task Management

### Creating Tasks

1. Navigate to **Tasks**
2. Click **New Task**
3. Specify:
   - **Title**: Clear task description
   - **Description**: Detailed information
   - **Priority**: Task urgency
   - **Agent Type**: Which agent should handle it
   - **Estimated Hours**: Time estimate

### Task Priorities

- **Critical**: Immediate attention required, blocks other work
- **High**: Important, should be completed soon
- **Medium**: Normal priority
- **Low**: Can be deferred if needed

### Task Lifecycle

```
Pending → In Progress → Completed/Failed
```

Tasks automatically:
- Get assigned to appropriate agents
- Update status in real-time
- Send notifications on completion
- Track execution metrics

### Filtering and Searching

Use filters to find specific tasks:
- By status (Pending, In Progress, Completed, Failed)
- By priority (Critical, High, Medium, Low)
- By agent type
- By date range

## Agent Coordination

### Running the Cognitive Loop

The cognitive loop executes all agents in sequence:

1. Navigate to **Agent Coordination**
2. Click **Execute Cognitive Loop**
3. Monitor progress in real-time
4. Review results for each agent

The loop typically completes in 30-60 seconds and provides:
- Strategic plan for the day
- Task execution results
- Knowledge gap analysis
- Innovation suggestions
- Performance insights

### Individual Agent Execution

Run specific agents when needed:

1. **Strategist**: Generate new strategic plans
   - Reviews current context
   - Prioritizes goals
   - Creates task breakdown

2. **Executor**: Execute pending tasks
   - Processes high-priority tasks first
   - Provides detailed execution logs
   - Updates task statuses

3. **Mentor**: Get guidance and identify gaps
   - Analyzes execution history
   - Identifies knowledge gaps
   - Provides improvement suggestions

4. **Innovator**: Generate creative solutions
   - Proposes innovative approaches
   - Suggests optimizations
   - Identifies opportunities

5. **Amplifier**: Analyze performance
   - Calculates key metrics
   - Identifies bottlenecks
   - Recommends optimizations

### Agent Synchronization

For coordinated execution:

1. Navigate to **Agent Coordination**
2. Select **Synchronize Strategic Agents**
3. Choose agents to synchronize
4. Set concurrency limit
5. Click **Execute**

This runs agents in a coordinated workflow, ensuring optimal execution order.

## Analytics and Insights

### Analytics Dashboard

Access comprehensive analytics:

1. Navigate to **Analytics**
2. Select time range (24h, 7d, 30d)
3. Review visualizations:

**Task Progress Chart**: 
- Shows completed, pending, and failed tasks over time
- Helps identify trends and bottlenecks

**Memory Usage Chart**:
- Displays memory distribution by type
- Helps optimize storage strategy

**Agent Activity Chart**:
- Shows agent workload and success rates
- Helps balance task distribution

**Performance Metrics**:
- Tracks latency and throughput
- Identifies performance degradation

### Interpreting Metrics

**Success Rate**: Percentage of successfully completed tasks
- Target: >95%
- Action if <90%: Review failed tasks, adjust task complexity

**Average Latency**: Time to complete typical requests
- Target: <500ms
- Action if >1000ms: Review caching, optimize queries

**Throughput**: Requests processed per second
- Varies by workload
- Monitor for sudden drops

### Exporting Data

Export analytics data for external analysis:

1. Click **Export** button
2. Choose format (CSV, JSON, Excel)
3. Select date range
4. Download file

## User Preferences

### Theme Settings

Customize your visual experience:

1. Navigate to **Settings** → **Appearance**
2. Choose theme:
   - **Light**: Optimal for bright environments
   - **Dark**: Reduces eye strain in low light
   - **System**: Matches your OS theme
3. Adjust font size (Small, Medium, Large)
4. Enable/disable compact mode

### Notification Settings

Control how JARVIS notifies you:

1. Navigate to **Settings** → **Notifications**
2. Configure:
   - Task completion notifications
   - Agent execution updates
   - Error alerts
   - Performance warnings
3. Choose notification method:
   - In-app notifications
   - Email notifications
   - WebSocket real-time updates

### Auto-Refresh Settings

Configure automatic data refresh:

1. Navigate to **Settings** → **General**
2. Enable auto-refresh
3. Set refresh interval (15s, 30s, 60s, 5min)
4. Choose which views to auto-refresh

## Advanced Features

### Memory Migration

When upgrading JARVIS, memory migration ensures data compatibility:

```python
from jarvis_core.application.services import MemoryMigration

# Validate all memories
report = await MemoryMigration.validate_repository_memories(
    repository=memory_repo,
    memory_type=MemoryType.STRATEGIC,
    fix_invalid=True
)

print(f"Valid: {report['valid']}")
print(f"Fixed: {report['fixed']}")
print(f"Failed: {report['failed']}")
```

### Custom Agent Workflows

Create custom agent workflows:

```python
from jarvis_core.application.services import AgentCoordinator

coordinator = AgentCoordinator(task_repository)

# Register agents
coordinator.register_agent(strategist)
coordinator.register_agent(executor)

# Execute coordinated workflow
result = await coordinator.synchronize_strategic_agents(context)
```

### API Integration

Integrate JARVIS with external systems:

```python
import requests

# API endpoint
base_url = "https://jarvis.example.com/api/v1"
headers = {"Authorization": f"Bearer {token}"}

# Create strategic goal
response = requests.post(
    f"{base_url}/memory/strategic/goals",
    json={
        "goal": "Integrate with CRM system",
        "priority": "high",
        "description": "Connect JARVIS to Salesforce"
    },
    headers=headers
)

goal = response.json()
```

### WebSocket Real-Time Updates

Connect to real-time updates:

```javascript
const ws = new WebSocket('wss://jarvis.example.com/ws');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  
  if (update.type === 'task_update') {
    console.log(`Task ${update.task_id} is now ${update.status}`);
  }
};
```

## Tips and Best Practices

### Strategic Goal Management

1. **Be Specific**: Clear goals are easier to track and achieve
2. **Set Realistic Timelines**: Allow buffer time for unexpected issues
3. **Define Measurable Metrics**: Use quantifiable success criteria
4. **Review Regularly**: Update progress weekly or bi-weekly
5. **Break Down Large Goals**: Use milestones for complex objectives

### Task Management

1. **Prioritize Ruthlessly**: Not everything is critical
2. **Estimate Conservatively**: Add buffer time to estimates
3. **Review Daily**: Check task progress daily
4. **Update Status Promptly**: Keep status current for accurate tracking
5. **Document Learnings**: Add notes about challenges and solutions

### Performance Optimization

1. **Monitor Regularly**: Check analytics weekly
2. **Address Trends**: Don't wait for major issues
3. **Test Changes**: Verify performance improvements
4. **Scale Appropriately**: Adjust resources based on load
5. **Cache Effectively**: Use caching for frequently accessed data

### Memory Management

1. **Archive Old Data**: Move completed items to archive
2. **Validate Regularly**: Run validation on strategic memory monthly
3. **Clean Up Duplicates**: Remove redundant entries
4. **Version Important Changes**: Track major decision changes
5. **Backup Frequently**: Maintain regular backups

### Team Collaboration

1. **Share Context**: Document decisions and rationale
2. **Use ADRs**: Maintain architectural consistency
3. **Review Together**: Conduct periodic team reviews
4. **Standardize Priorities**: Align on priority definitions
5. **Communicate Changes**: Keep team informed of updates

## Keyboard Shortcuts

Speed up your workflow with keyboard shortcuts:

- `Ctrl/Cmd + K`: Quick search
- `Ctrl/Cmd + N`: New task
- `Ctrl/Cmd + G`: New strategic goal
- `Ctrl/Cmd + E`: Execute cognitive loop
- `Ctrl/Cmd + ,`: Open settings
- `Ctrl/Cmd + /`: Show shortcuts help
- `Escape`: Close modals
- `Ctrl/Cmd + S`: Save current form

## Getting Help

### In-App Help

- Click the **?** icon in the top right
- Hover over labels for tooltips
- Check the **Help** section for guides

### Documentation

- User Guide: This document
- API Documentation: `/docs/API_DOCUMENTATION.md`
- Deployment Guide: `/docs/DEPLOYMENT_GUIDE.md`
- Architecture Overview: `/docs/architecture/`

### Support Channels

- GitHub Issues: Report bugs and request features
- Email Support: support@jarvis-ai.example.com
- Community Forum: https://community.jarvis-ai.example.com

## Troubleshooting

### Common Issues

**Tasks not executing:**
- Check agent status in dashboard
- Verify task priority and status
- Review error logs in analytics

**Slow performance:**
- Check system resources
- Review database performance
- Clear cache and restart

**Data not syncing:**
- Verify network connection
- Check WebSocket status
- Refresh the page

**Authentication issues:**
- Clear browser cache
- Refresh auth token
- Contact support if persists

## What's Next?

Now that you're familiar with JARVIS basics:

1. Create your first strategic goal
2. Add some tasks and let agents execute them
3. Explore the analytics dashboard
4. Customize your preferences
5. Set up integrations with your tools

Happy cognitive assisting! 🚀
