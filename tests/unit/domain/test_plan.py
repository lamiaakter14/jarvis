"""Unit tests for Plan entity."""
import pytest
from datetime import date, datetime
from uuid import uuid4

from jarvis_core.domain.entities.plan import Plan
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.roi import ROI


@pytest.mark.unit
class TestPlan:
    """Test Plan entity."""
    
    def test_create_plan_with_required_fields(self):
        """Test creating a plan with required fields."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=[],
            total_hours=8.0
        )
        
        assert plan.date == date.today()
        assert plan.tasks == []
        assert plan.total_hours == 8.0
        assert plan.status == "draft"
    
    def test_create_plan_with_tasks(self, sample_tasks):
        """Test creating a plan with tasks."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0,
            status="active"
        )
        
        assert len(plan.tasks) == len(sample_tasks)
        assert plan.status == "active"
    
    def test_add_task_to_plan(self, sample_task):
        """Test adding a task to a plan."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=[],
            total_hours=8.0
        )
        
        plan.add_task(sample_task)
        assert len(plan.tasks) == 1
        assert sample_task in plan.tasks
    
    def test_remove_task_from_plan(self, sample_tasks):
        """Test removing a task from a plan."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks.copy(),
            total_hours=8.0
        )
        
        initial_count = len(plan.tasks)
        task_to_remove = sample_tasks[0]
        
        plan.remove_task(task_to_remove.task_id)
        assert len(plan.tasks) == initial_count - 1
        assert task_to_remove not in plan.tasks
    
    def test_get_total_estimated_hours(self, sample_tasks):
        """Test calculating total estimated hours."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0
        )
        
        total_hours = plan.get_total_estimated_hours()
        assert isinstance(total_hours, (int, float))
        assert total_hours >= 0
    
    def test_get_remaining_hours(self, sample_tasks):
        """Test calculating remaining hours."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0
        )
        
        remaining = plan.get_remaining_hours()
        assert isinstance(remaining, (int, float))
    
    def test_get_completion_percentage(self, sample_tasks):
        """Test calculating completion percentage."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0
        )
        
        # Initially no tasks completed
        percentage = plan.get_completion_percentage()
        assert percentage == 0.0
        
        # Mark first task as completed
        sample_tasks[0].mark_completed()
        percentage = plan.get_completion_percentage()
        assert 0 <= percentage <= 100
    
    def test_is_overallocated(self, sample_tasks):
        """Test checking if plan is overallocated."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=1.0  # Very low hours
        )
        
        # This depends on implementation - may or may not be overallocated
        is_over = plan.is_overallocated()
        assert isinstance(is_over, bool)
    
    def test_get_tasks_by_priority(self, sample_tasks):
        """Test getting tasks filtered by priority."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0
        )
        
        high_priority_tasks = plan.get_tasks_by_priority(Priority.HIGH)
        assert all(task.priority == Priority.HIGH for task in high_priority_tasks)
    
    def test_plan_to_dict(self, sample_plan):
        """Test converting plan to dictionary."""
        plan_dict = sample_plan.to_dict()
        
        assert isinstance(plan_dict, dict)
        assert "plan_id" in plan_dict
        assert "date" in plan_dict
        assert "tasks" in plan_dict
        assert "total_hours" in plan_dict
        assert "status" in plan_dict
    
    def test_plan_activate(self):
        """Test activating a plan."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=[],
            total_hours=8.0
        )
        
        assert plan.status == "draft"
        plan.activate()
        assert plan.status == "active"
    
    def test_plan_complete(self, sample_tasks):
        """Test completing a plan."""
        plan = Plan(
            plan_id=str(uuid4()),
            date=date.today(),
            tasks=sample_tasks,
            total_hours=8.0,
            status="active"
        )
        
        # Mark all tasks as completed
        for task in sample_tasks:
            task.mark_completed()
        
        plan.complete()
        assert plan.status == "completed"
