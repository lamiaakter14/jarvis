"""Unit tests for Task entity."""

from datetime import datetime
from uuid import uuid4

import pytest
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI


@pytest.mark.unit
class TestTask:
    """Test Task entity."""

    def test_create_task_with_required_fields(self):
        """Test creating a task with required fields."""
        task = Task(
            task_id=str(uuid4()),
            title="Test Task",
            description="Test Description",
            priority=Priority.HIGH,
            cognitive_load=CognitiveLoad.MEDIUM,
            roi=ROI(0.8),
        )

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == Priority.HIGH
        assert task.cognitive_load == CognitiveLoad.MEDIUM
        assert task.roi.value == 0.8
        assert task.status == "pending"

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields."""
        now = datetime.now()
        task_id = str(uuid4())

        task = Task(
            task_id=task_id,
            title="Complete Task",
            description="Detailed description",
            priority=Priority.CRITICAL,
            cognitive_load=CognitiveLoad.HIGH,
            roi=ROI(0.95),
            status="completed",
            agent_type=AgentType.EXECUTOR,
            created_at=now,
            completed_at=now,
            result={"success": True},
        )

        assert task.task_id == task_id
        assert task.title == "Complete Task"
        assert task.priority == Priority.CRITICAL
        assert task.cognitive_load == CognitiveLoad.HIGH
        assert task.status == "completed"
        assert task.agent_type == AgentType.EXECUTOR
        assert task.result == {"success": True}

    def test_task_equality(self):
        """Test task equality based on task_id."""
        task_id = str(uuid4())
        task1 = Task(
            task_id=task_id,
            title="Task 1",
            description="Desc 1",
            priority=Priority.HIGH,
            cognitive_load=CognitiveLoad.MEDIUM,
            roi=ROI(0.8),
        )
        task2 = Task(
            task_id=task_id,
            title="Task 2",  # Different title
            description="Desc 2",
            priority=Priority.LOW,
            cognitive_load=CognitiveLoad.LOW,
            roi=ROI(0.5),
        )

        assert task1 == task2  # Same ID means equal

    def test_task_to_dict(self, sample_task):
        """Test converting task to dictionary."""
        task_dict = sample_task.to_dict()

        assert isinstance(task_dict, dict)
        assert "task_id" in task_dict
        assert "title" in task_dict
        assert "description" in task_dict
        assert "priority" in task_dict
        assert "cognitive_load" in task_dict
        assert "roi" in task_dict
        assert task_dict["title"] == sample_task.title

    def test_task_mark_completed(self, sample_task):
        """Test marking task as completed."""
        sample_task.mark_completed(result={"success": True, "output": "Done"})

        assert sample_task.status == "completed"
        assert sample_task.completed_at is not None
        assert sample_task.result == {"success": True, "output": "Done"}

    def test_task_mark_failed(self, sample_task):
        """Test marking task as failed."""
        sample_task.mark_failed(error="Test error occurred")

        assert sample_task.status == "failed"
        assert sample_task.result == {"error": "Test error occurred"}

    def test_task_mark_in_progress(self, sample_task):
        """Test marking task as in progress."""
        assert sample_task.status == "pending"
        sample_task.mark_in_progress()
        assert sample_task.status == "in_progress"

    def test_task_is_completed(self, sample_task):
        """Test checking if task is completed."""
        assert not sample_task.is_completed()

        sample_task.mark_completed()
        assert sample_task.is_completed()

    def test_task_is_pending(self, sample_task):
        """Test checking if task is pending."""
        assert sample_task.is_pending()

        sample_task.mark_in_progress()
        assert not sample_task.is_pending()

    def test_task_get_estimated_hours(self, sample_task):
        """Test getting estimated hours for task."""
        hours = sample_task.get_estimated_hours()
        assert isinstance(hours, (int, float))
        assert hours > 0
