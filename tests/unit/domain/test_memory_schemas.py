"""Unit tests for memory content schemas."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from jarvis_core.domain.schemas.memory_content import (
    WorkingMemoryContent,
    KnowledgeMemoryContent,
    StrategicMemoryContent,
    ExecutionLogContent,
    ADRContent,
    validate_memory_content
)


@pytest.mark.unit
class TestWorkingMemoryContent:
    """Test WorkingMemoryContent schema."""
    
    def test_create_working_memory_content(self):
        """Test creating valid working memory content."""
        content = WorkingMemoryContent(
            data={"key": "value"},
            session_id="session_123",
            agent_id="agent_456"
        )
        
        assert content.data == {"key": "value"}
        assert content.session_id == "session_123"
        assert content.agent_id == "agent_456"
    
    def test_working_memory_content_requires_data(self):
        """Test that data field is required."""
        with pytest.raises(ValidationError):
            WorkingMemoryContent()  # type: ignore
    
    def test_working_memory_content_allows_extra_fields(self):
        """Test that extra fields are allowed."""
        content = WorkingMemoryContent(
            data={"key": "value"},
            custom_field="custom_value"
        )
        
        assert content.data == {"key": "value"}


@pytest.mark.unit
class TestKnowledgeMemoryContent:
    """Test KnowledgeMemoryContent schema."""
    
    def test_create_knowledge_memory_content(self):
        """Test creating valid knowledge memory content."""
        content = KnowledgeMemoryContent(
            title="Test Knowledge",
            content="This is test knowledge",
            category="testing",
            tags=["test", "sample"],
            confidence=0.95
        )
        
        assert content.title == "Test Knowledge"
        assert content.content == "This is test knowledge"
        assert content.category == "testing"
        assert len(content.tags) == 2
        assert content.confidence == 0.95
    
    def test_knowledge_content_validates_confidence_range(self):
        """Test that confidence is validated to be between 0 and 1."""
        with pytest.raises(ValidationError):
            KnowledgeMemoryContent(
                title="Test",
                content="Test",
                confidence=1.5
            )
        
        with pytest.raises(ValidationError):
            KnowledgeMemoryContent(
                title="Test",
                content="Test",
                confidence=-0.1
            )
    
    def test_knowledge_content_default_values(self):
        """Test default values in knowledge content."""
        content = KnowledgeMemoryContent(
            title="Test",
            content="Test"
        )
        
        assert content.description == ""
        assert content.tags == []
        assert content.confidence == 1.0
        assert content.access_count == 0


@pytest.mark.unit
class TestStrategicMemoryContent:
    """Test StrategicMemoryContent schema."""
    
    def test_create_strategic_memory_content(self):
        """Test creating valid strategic memory content."""
        content = StrategicMemoryContent(
            goal="Complete project milestone",
            description="Finish phase 1",
            priority="high",
            status="active",
            progress=50.0
        )
        
        assert content.goal == "Complete project milestone"
        assert content.priority == "high"
        assert content.status == "active"
        assert content.progress == 50.0
    
    def test_strategic_content_validates_priority(self):
        """Test that priority is validated."""
        with pytest.raises(ValidationError, match="Priority must be one of"):
            StrategicMemoryContent(
                goal="Test",
                priority="invalid"
            )
    
    def test_strategic_content_validates_status(self):
        """Test that status is validated."""
        with pytest.raises(ValidationError, match="Status must be one of"):
            StrategicMemoryContent(
                goal="Test",
                priority="high",
                status="invalid"
            )
    
    def test_strategic_content_validates_progress_range(self):
        """Test that progress is validated to be between 0 and 100."""
        with pytest.raises(ValidationError):
            StrategicMemoryContent(
                goal="Test",
                priority="high",
                progress=150.0
            )
        
        with pytest.raises(ValidationError):
            StrategicMemoryContent(
                goal="Test",
                priority="high",
                progress=-10.0
            )
    
    def test_strategic_content_default_values(self):
        """Test default values in strategic content."""
        content = StrategicMemoryContent(
            goal="Test Goal",
            priority="medium"
        )
        
        assert content.status == "active"
        assert content.progress == 0.0
        assert content.milestones == []
        assert content.dependencies == []
        assert content.metrics == {}


@pytest.mark.unit
class TestExecutionLogContent:
    """Test ExecutionLogContent schema."""
    
    def test_create_execution_log_content(self):
        """Test creating valid execution log content."""
        content = ExecutionLogContent(
            task_id="task_123",
            task_title="Test Task",
            status="completed",
            started_at=datetime.now(),
            duration_seconds=30.5
        )
        
        assert content.task_id == "task_123"
        assert content.task_title == "Test Task"
        assert content.status == "completed"
        assert content.duration_seconds == 30.5
    
    def test_execution_log_validates_status(self):
        """Test that status is validated."""
        with pytest.raises(ValidationError, match="Status must be one of"):
            ExecutionLogContent(
                task_id="task_123",
                task_title="Test",
                status="invalid",
                started_at=datetime.now()
            )
    
    def test_execution_log_validates_duration(self):
        """Test that duration cannot be negative."""
        with pytest.raises(ValidationError):
            ExecutionLogContent(
                task_id="task_123",
                task_title="Test",
                status="completed",
                started_at=datetime.now(),
                duration_seconds=-10.0
            )


@pytest.mark.unit
class TestADRContent:
    """Test ADRContent schema."""
    
    def test_create_adr_content(self):
        """Test creating valid ADR content."""
        content = ADRContent(
            title="Use PostgreSQL for database",
            status="accepted",
            date=datetime.now(),
            context="We need a reliable database",
            decision="Use PostgreSQL",
            consequences="Strong consistency, ACID compliance",
            alternatives=["MySQL", "MongoDB"]
        )
        
        assert content.title == "Use PostgreSQL for database"
        assert content.status == "accepted"
        assert content.decision == "Use PostgreSQL"
        assert len(content.alternatives) == 2
    
    def test_adr_validates_status(self):
        """Test that ADR status is validated."""
        with pytest.raises(ValidationError, match="Status must be one of"):
            ADRContent(
                title="Test",
                status="invalid",
                date=datetime.now(),
                context="Context",
                decision="Decision",
                consequences="Consequences"
            )
    
    def test_adr_default_values(self):
        """Test default values in ADR."""
        content = ADRContent(
            title="Test ADR",
            date=datetime.now(),
            context="Context",
            decision="Decision",
            consequences="Consequences"
        )
        
        assert content.status == "proposed"
        assert content.alternatives == []
        assert content.related_decisions == []
        assert content.superseded_by is None


@pytest.mark.unit
class TestValidateMemoryContent:
    """Test validate_memory_content function."""
    
    def test_validate_working_memory(self):
        """Test validating working memory content."""
        content_dict = {
            "data": {"key": "value"},
            "session_id": "session_123"
        }
        
        result = validate_memory_content("working", content_dict)
        
        assert isinstance(result, WorkingMemoryContent)
        assert result.data == {"key": "value"}
    
    def test_validate_knowledge_memory(self):
        """Test validating knowledge memory content."""
        content_dict = {
            "title": "Test",
            "content": "Test content"
        }
        
        result = validate_memory_content("knowledge", content_dict)
        
        assert isinstance(result, KnowledgeMemoryContent)
        assert result.title == "Test"
    
    def test_validate_strategic_memory(self):
        """Test validating strategic memory content."""
        content_dict = {
            "goal": "Test Goal",
            "priority": "high"
        }
        
        result = validate_memory_content("strategic", content_dict)
        
        assert isinstance(result, StrategicMemoryContent)
        assert result.goal == "Test Goal"
    
    def test_validate_execution_log(self):
        """Test validating execution log content."""
        content_dict = {
            "task_id": "task_123",
            "task_title": "Test",
            "status": "completed",
            "started_at": datetime.now()
        }
        
        result = validate_memory_content("execution_log", content_dict)
        
        assert isinstance(result, ExecutionLogContent)
        assert result.task_id == "task_123"
    
    def test_validate_adr(self):
        """Test validating ADR content."""
        content_dict = {
            "title": "Test ADR",
            "date": datetime.now(),
            "context": "Test context",
            "decision": "Test decision",
            "consequences": "Test consequences"
        }
        
        result = validate_memory_content("adr", content_dict)
        
        assert isinstance(result, ADRContent)
        assert result.title == "Test ADR"
    
    def test_validate_unknown_memory_type(self):
        """Test that unknown memory type raises error."""
        with pytest.raises(ValueError, match="Unknown memory type"):
            validate_memory_content("unknown", {})
    
    def test_validate_invalid_content(self):
        """Test that invalid content raises validation error."""
        with pytest.raises(ValidationError):
            validate_memory_content("knowledge", {
                "title": "Test"
                # Missing required 'content' field
            })
