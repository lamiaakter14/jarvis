# Strategic Memory

This directory contains strategic planning documents, long-term goals, milestones, and architecture decision records (ADRs) for the JARVIS project.

## Overview

Strategic memory is a critical component of JARVIS that captures the vision, roadmap, and key architectural decisions that guide the project's development. Unlike working memory (temporary task data) or knowledge memory (learned information), strategic memory provides the long-term direction and decision history.

## Directory Structure

```
strategic/
├── README.md                           # This file
├── long_term_goal.md                   # Vision and long-term goals
├── milestones.md                       # Concrete milestones and deliverables
└── architecture_decision_records/      # ADRs directory
    ├── 001-clean-architecture.md       # ADR for clean architecture adoption
    └── 002-schema-validation.md        # ADR for schema validation
```

## Files

### 1. Long-Term Goals (`long_term_goal.md`)

**Purpose**: Defines the overarching vision and strategic goals for JARVIS.

**Contents**:
- **Vision Statement**: What JARVIS aims to become
- **Year 1 Goals**: Foundation, Enhancement, and Intelligence phases
  - Q1-Q2: Fundamentals (Phase 1)
  - Q3: Enhancement (Phase 2)
  - Q4: Intelligence (Phase 3)
- **Year 2 Goals**: Scaling and Leveraging phases
  - Q1-Q2: Scaling (Phase 4)
  - Q3-Q4: Leveraging (Phase 5)
- **Beyond Year 2**: Long-term vision and moonshot goals

**Key Metrics**:
- Success criteria for each phase
- Quantitative targets (e.g., code coverage, user count, performance)
- Qualitative objectives (e.g., developer experience, system capabilities)

### 2. Milestones (`milestones.md`)

**Purpose**: Tracks concrete milestones and deliverables across development phases.

**Contents**:
- **Phase 1: Foundation** (6 months)
  - Milestone 1.1: Core Architecture Setup ✅
  - Milestone 1.2: Agent Implementation ✅
  - Milestone 1.3: Cognitive Loop Development ✅
  - Milestone 1.4: Memory Management System 🔄
  - Milestone 1.5: Testing and Documentation
  
- **Phase 2: Enhancement** (3 months)
  - Agent Collaboration Enhancement
  - Performance Optimization
  - Knowledge Base Expansion
  - User Feedback System
  
- **Phase 3: Intelligence** (3 months)
  - Machine Learning Integration
  - Predictive Analytics
  - Contextual Awareness
  - NLU Improvements
  - Recommendation Engine
  
- **Phase 4: Scaling** (6 months)
  - Multi-User Architecture
  - Collaborative Features
  - Enterprise Security
  - API Ecosystem
  - Distributed Architecture

**Status Indicators**:
- ✅ Completed
- 🔄 In Progress
- [ ] Planned

### 3. Architecture Decision Records (ADRs)

**Purpose**: Documents important architectural decisions with context, consequences, and rationale.

**Format**: Each ADR follows a standard structure:
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: Decision date
- **Context**: Background and motivation
- **Decision**: What was decided
- **Consequences**: Positive and negative outcomes
- **Alternatives Considered**: Other options and why they were rejected

#### ADR-001: Clean Architecture

**Topic**: Adoption of Clean Architecture principles  
**Status**: Accepted  
**Key Decision**: Implement layered architecture with strict dependency rules

**Layers**:
1. Entities (Core Domain)
2. Use Cases (Application Business Rules)
3. Interface Adapters
4. Frameworks & Drivers

**Benefits**:
- Independent testability
- Framework independence
- Database independence
- UI independence

#### ADR-002: Schema Validation

**Topic**: Schema validation for memory management system  
**Status**: Accepted  
**Key Decision**: Use Pydantic for runtime schema validation

**Benefits**:
- Data integrity guarantees
- Type safety and IDE support
- Self-documenting schemas
- JSON Schema generation
- Migration support

**Implementation**:
- Pydantic models for all memory types
- Validation on save operations
- Schema versioning strategy
- Migration utilities

## Usage

### Accessing Strategic Memory (via MemoryManager)

```python
from core.memory_manager import MemoryManager

# Initialize memory manager
memory = MemoryManager()

# Read long-term goals
goals = memory.get_strategic_file("long_term_goal.md")
print(goals)

# Read milestones
milestones = memory.get_strategic_file("milestones.md")
print(milestones)

# List all ADRs
adrs = memory.list_adrs()
print(f"Available ADRs: {adrs}")

# Read a specific ADR
adr_001 = memory.get_adr("001")
print(adr_001)

adr_002 = memory.get_adr("002")
print(adr_002)
```

### Validation

Run the validation script to ensure all strategic memory files are properly populated:

```bash
python scripts/validate_strategic_memory.py
```

This script checks:
- File existence
- Minimum content requirements
- MemoryManager API functionality
- Accessibility of all strategic documents

## Adding New ADRs

When making significant architectural decisions, create a new ADR:

1. **Create a new file**: `architecture_decision_records/XXX-title.md`
   - Use sequential numbering (003, 004, etc.)
   - Use kebab-case for the title

2. **Follow the ADR template**:
   ```markdown
   # ADR XXX: [Title]
   
   **Status**: [Proposed|Accepted|Deprecated|Superseded]
   **Date**: YYYY-MM
   **Deciders**: [Who made the decision]
   
   ## Context
   [Background and problem statement]
   
   ## Decision
   [What was decided and why]
   
   ## Consequences
   ### Positive
   - [Benefits]
   
   ### Negative
   - [Drawbacks]
   
   ## Alternatives Considered
   - [Alternative 1]: [Why rejected]
   - [Alternative 2]: [Why rejected]
   
   ## References
   - [Relevant links and documents]
   ```

3. **Update milestones.md** if the decision affects the roadmap

4. **Commit with descriptive message**: `Add ADR-XXX: [Title]`

## Maintaining Strategic Memory

### Review Cycle

- **Monthly**: Review milestone progress
- **Quarterly**: Update goals and adjust roadmap
- **Per Phase**: Review and update ADRs as needed

### Ownership

- **Long-term Goals**: Product Lead, Technical Lead
- **Milestones**: Project Manager, Development Team Leads
- **ADRs**: Technical Lead, Architecture Review Board

### Version Control

All strategic memory files are version controlled in Git:
- Track changes over time
- Review history of decisions
- Understand evolution of strategy

## Integration with Other Memory Types

Strategic memory complements other memory types:

| Memory Type | Purpose | Format | Examples |
|-------------|---------|--------|----------|
| **Working** | Active tasks and execution | JSON | daily_context.json, task_queue.json |
| **Knowledge** | Learning and reflections | Markdown + YAML | learning_logs.md, reflections.md |
| **Strategic** | Goals and decisions | Markdown | long_term_goal.md, ADRs |

## Benefits of Strategic Memory

1. **Alignment**: Ensures all development aligns with long-term vision
2. **Decision History**: Provides context for why decisions were made
3. **Onboarding**: Helps new team members understand project direction
4. **Accountability**: Tracks commitments and progress toward goals
5. **Learning**: Documents what worked and what didn't
6. **Communication**: Clear reference for stakeholders

## Related Documentation

- [README.md](/README.md) - Project overview
- [WORKFLOW.md](/WORKFLOW.md) - Git workflow documentation
- [roadmap.md](/memory/knowledge/roadmap.md) - High-level project roadmap

---

**Last Updated**: February 2024  
**Next Review**: End of Milestone 1.4
