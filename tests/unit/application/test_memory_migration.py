"""Tests for memory migration service."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from jarvis_core.application.services.memory_migration import (
    MemoryMigration,
    MigrationError
)
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType


@pytest.mark.unit
class TestMemoryMigration:
    """Unit tests for memory migration service."""
    
    def test_validate_valid_strategic_memory(self):
        """Test validation of valid strategic memory."""
        memory = Memory(
            key="goal_test_001",
            type=MemoryType.STRATEGIC,
            content={
                "goal": "Complete JARVIS project",
                "priority": "high",
                "status": "active",
                "description": "Final implementation",
                "progress": 75.0,
                "milestones": [],
                "dependencies": [],
                "metrics": {}
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) == 0
        assert fixed_memory.content["goal"] == "Complete JARVIS project"
    
    def test_fix_missing_required_fields_strategic(self):
        """Test fixing strategic memory with missing required fields."""
        memory = Memory(
            key="goal_test_002",
            type=MemoryType.STRATEGIC,
            content={}  # Missing required fields
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) > 0
        assert fixed_memory.content["goal"] == "Unspecified Goal"
        assert fixed_memory.content["priority"] == "medium"
        assert fixed_memory.content["status"] == "active"
    
    def test_fix_invalid_priority(self):
        """Test fixing strategic memory with invalid priority."""
        memory = Memory(
            key="goal_test_003",
            type=MemoryType.STRATEGIC,
            content={
                "goal": "Test goal",
                "priority": "invalid",  # Invalid priority
                "status": "active"
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert fixed_memory.content["priority"] == "medium"
        assert any("priority" in fix.lower() for fix in fixes)
    
    def test_fix_invalid_status(self):
        """Test fixing strategic memory with invalid status."""
        memory = Memory(
            key="goal_test_004",
            type=MemoryType.STRATEGIC,
            content={
                "goal": "Test goal",
                "priority": "high",
                "status": "invalid"  # Invalid status
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert fixed_memory.content["status"] == "active"
        assert any("status" in fix.lower() for fix in fixes)
    
    def test_fix_progress_out_of_range(self):
        """Test fixing strategic memory with progress out of range."""
        memory = Memory(
            key="goal_test_005",
            type=MemoryType.STRATEGIC,
            content={
                "goal": "Test goal",
                "priority": "high",
                "status": "active",
                "progress": 150.0  # Out of range
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert 0 <= fixed_memory.content["progress"] <= 100
        assert any("progress" in fix.lower() for fix in fixes)
    
    def test_validate_valid_knowledge(self):
        """Test validation of valid knowledge memory."""
        memory = Memory(
            key="know_test_001",
            type=MemoryType.KNOWLEDGE,
            content={
                "title": "Python Best Practices",
                "content": "Use type hints",
                "description": "Guidelines for Python",
                "tags": ["python", "best-practices"],
                "confidence": 0.9
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) == 0
        assert fixed_memory.content["title"] == "Python Best Practices"
    
    def test_fix_missing_knowledge_fields(self):
        """Test fixing knowledge memory with missing fields."""
        memory = Memory(
            key="know_test_002",
            type=MemoryType.KNOWLEDGE,
            content={}
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) > 0
        assert "title" in fixed_memory.content
        assert "content" in fixed_memory.content
    
    def test_fix_confidence_out_of_range(self):
        """Test fixing knowledge memory with confidence out of range."""
        memory = Memory(
            key="know_test_003",
            type=MemoryType.KNOWLEDGE,
            content={
                "title": "Test",
                "content": "Test",
                "confidence": 1.5  # Out of range
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert 0 <= fixed_memory.content["confidence"] <= 1
        assert any("confidence" in fix.lower() for fix in fixes)
    
    def test_validate_valid_execution_log(self):
        """Test validation of valid execution log memory."""
        memory = Memory(
            key="exec_test_001",
            type=MemoryType.EXECUTION_LOG,
            content={
                "task_id": "task_123",
                "task_title": "Test Task",
                "status": "completed",
                "started_at": datetime.now(),
                "metrics": {}
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) == 0
        assert fixed_memory.content["task_id"] == "task_123"
    
    def test_fix_missing_execution_log_fields(self):
        """Test fixing execution log memory with missing fields."""
        memory = Memory(
            key="exec_test_002",
            type=MemoryType.EXECUTION_LOG,
            content={}
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) > 0
        assert "task_id" in fixed_memory.content
        assert "task_title" in fixed_memory.content
        assert "status" in fixed_memory.content
    
    def test_validate_valid_working_memory(self):
        """Test validation of valid working memory."""
        memory = Memory(
            key="work_test_001",
            type=MemoryType.WORKING,
            content={
                "data": {"key": "value"}
            }
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) == 0
        assert "data" in fixed_memory.content
    
    def test_fix_missing_working_memory_data(self):
        """Test fixing working memory with missing data field."""
        memory = Memory(
            key="work_test_002",
            type=MemoryType.WORKING,
            content={}
        )
        
        fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
        
        assert len(fixes) > 0
        assert "data" in fixed_memory.content
        assert isinstance(fixed_memory.content["data"], dict)
    
    @pytest.mark.asyncio
    async def test_migrate_memory_same_version(self):
        """Test migrating memory to same version."""
        memory = Memory(
            key="migrate_test_001",
            type=MemoryType.STRATEGIC,
            content={
                "goal": "Test",
                "priority": "medium",
                "status": "active"
            }
        )
        memory.metadata["schema_version"] = 1
        
        migrated, migrations = await MemoryMigration.migrate_memory(memory, 1)
        
        assert len(migrations) == 0
        assert migrated.metadata["schema_version"] == 1
