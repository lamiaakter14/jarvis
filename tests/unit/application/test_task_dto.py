"""Unit tests for TaskDTO."""
import pytest
from datetime import datetime
from uuid import uuid4

from jarvis_core.application.dto.task_dto import TaskDTO
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.domain.value_objects.agent_type import AgentType


@pytest.mark.unit
class TestTaskDTO:
    """Test TaskDTO."""
    
    def test_create_task_dto(self):
        """Test creating a TaskDTO."""
        dto = TaskDTO(
            task_id=str(uuid4()),
            title="Test Task",
            description="Test Description",
            priority="high",
            cognitive_load="medium",
            roi=0.8,
            status="pending"
        )
        
        assert dto.title == "Test Task"
        assert dto.priority == "high"
        assert dto.roi == 0.8
    
    def test_task_dto_from_entity(self, sample_task):
        """Test creating TaskDTO from Task entity."""
        dto = TaskDTO.from_entity(sample_task)
        
        assert dto.task_id == sample_task.task_id
        assert dto.title == sample_task.title
        assert dto.description == sample_task.description
        assert dto.status == sample_task.status
    
    def test_task_dto_to_entity(self):
        """Test converting TaskDTO to Task entity."""
        dto = TaskDTO(
            task_id=str(uuid4()),
            title="Test Task",
            description="Test Description",
            priority="high",
            cognitive_load="medium",
            roi=0.8,
            status="pending",
            agent_type="executor"
        )
        
        task = dto.to_entity()
        
        assert isinstance(task, Task)
        assert task.task_id == dto.task_id
        assert task.title == dto.title
        assert task.priority == Priority.HIGH
        assert task.cognitive_load == CognitiveLoad.MEDIUM
    
    def test_task_dto_to_dict(self):
        """Test converting TaskDTO to dictionary."""
        dto = TaskDTO(
            task_id=str(uuid4()),
            title="Test Task",
            description="Test Description",
            priority="high",
            cognitive_load="medium",
            roi=0.8,
            status="pending"
        )
        
        task_dict = dto.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict["title"] == "Test Task"
        assert task_dict["priority"] == "high"
    
    def test_task_dto_roundtrip(self, sample_task):
        """Test entity -> DTO -> entity roundtrip."""
        # Entity to DTO
        dto = TaskDTO.from_entity(sample_task)
        
        # DTO back to entity
        task = dto.to_entity()
        
        # Verify key fields match
        assert task.task_id == sample_task.task_id
        assert task.title == sample_task.title
        assert task.priority == sample_task.priority
    
    def test_task_dto_validation(self):
        """Test TaskDTO validation with Pydantic."""
        # Valid DTO
        dto = TaskDTO(
            task_id=str(uuid4()),
            title="Test",
            description="Test",
            priority="high",
            cognitive_load="medium",
            roi=0.8,
            status="pending"
        )
        assert dto is not None
        
        # Invalid ROI (if validation is set up)
        with pytest.raises((ValueError, Exception)):
            TaskDTO(
                task_id=str(uuid4()),
                title="Test",
                description="Test",
                priority="high",
                cognitive_load="medium",
                roi=1.5,  # Invalid: > 1.0
                status="pending"
            )
