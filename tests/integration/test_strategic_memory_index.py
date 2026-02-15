"""Integration tests for strategic memory indexed storage."""

import pytest
from datetime import datetime
import tempfile
import shutil

from jarvis_core.application.use_cases.manage_strategic_memory import ManageStrategicMemory
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
from jarvis_core.shared.constants import MemoryType


@pytest.mark.integration
class TestStrategicMemoryIndexedStorage:
    """Integration tests for indexed strategic memory storage."""
    
    @pytest.fixture
    def temp_memory_dir(self):
        """Create temporary directory for memory storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def repository(self, temp_memory_dir):
        """Create repository instance."""
        return FileMemoryRepository(base_path=temp_memory_dir)
    
    @pytest.fixture
    def use_case(self, repository):
        """Create use case instance."""
        return ManageStrategicMemory(repository)
    
    @pytest.mark.asyncio
    async def test_index_updated_on_goal_creation(self, use_case, repository):
        """Test that index is updated when creating a goal."""
        # Create a goal
        goal = await use_case.create_strategic_goal(
            goal="Test indexed goal",
            description="Testing index updates",
            priority="high"
        )
        
        # Verify goal is in the index
        index = repository.strategic_index
        assert goal.key in index.find_by_type("goal")
        assert goal.key in index.find_by_priority("high")
        assert goal.key in index.find_by_status("active")
        assert goal.key in index.find_by_tag("strategic")
        assert goal.key in index.find_by_tag("high")
    
    @pytest.mark.asyncio
    async def test_index_updated_on_adr_creation(self, use_case, repository):
        """Test that index is updated when creating an ADR."""
        # Create an ADR
        adr = await use_case.create_adr(
            title="Test indexed ADR",
            context="Testing index for ADRs",
            decision="Use indexed storage",
            consequences="Fast retrieval",
            status="proposed"
        )
        
        # Verify ADR is in the index
        index = repository.strategic_index
        assert adr.key in index.find_by_type("adr")
        assert adr.key in index.find_by_status("proposed")
        assert adr.key in index.find_by_tag("adr")
        assert adr.key in index.find_by_tag("architecture")
    
    @pytest.mark.asyncio
    async def test_index_search_performance(self, use_case, repository):
        """Test that index improves search performance for tag-based queries."""
        # Create multiple goals with different tags
        goals = []
        for i in range(5):
            goal = await use_case.create_strategic_goal(
                goal=f"Performance goal {i}",
                priority="high" if i % 2 == 0 else "medium",
                milestones=[{"name": f"Milestone {i}"}]
            )
            goals.append(goal)
        
        # Search using tags (should use index fast path)
        results = await repository.search(
            memory_type=MemoryType.STRATEGIC,
            tags=["high"]
        )
        
        # Verify results
        assert len(results) == 3  # 3 high priority goals (0, 2, 4)
        assert all(r.has_tag("high") for r in results)
    
    @pytest.mark.asyncio
    async def test_index_updated_on_goal_update(self, use_case, repository):
        """Test that index is updated when updating a goal."""
        # Create a goal
        goal = await use_case.create_strategic_goal(
            goal="Test update",
            priority="low"
        )
        
        # Verify initial state
        index = repository.strategic_index
        assert goal.key in index.find_by_priority("low")
        assert goal.key not in index.find_by_priority("high")
        
        # Update goal with new priority (indirectly by saving)
        goal.content["priority"] = "high"
        await repository.save(goal)
        
        # Verify index was updated
        assert goal.key not in index.find_by_priority("low")
        assert goal.key in index.find_by_priority("high")
    
    @pytest.mark.asyncio
    async def test_index_removed_on_deletion(self, use_case, repository):
        """Test that index is updated when deleting a memory."""
        # Create a goal
        goal = await use_case.create_strategic_goal(
            goal="Test deletion",
            priority="high"
        )
        
        # Verify in index
        index = repository.strategic_index
        assert goal.key in index.find_by_type("goal")
        
        # Delete the goal
        await repository.delete(goal.key)
        
        # Verify removed from index
        assert goal.key not in index.find_by_type("goal")
        assert goal.key not in index.find_by_priority("high")
        assert goal.key not in index.find_by_status("active")
    
    @pytest.mark.asyncio
    async def test_index_persistence(self, temp_memory_dir, use_case):
        """Test that index persists across repository instances."""
        # Create some goals and ADRs
        goal = await use_case.create_strategic_goal(
            goal="Persistent goal",
            priority="high"
        )
        adr = await use_case.create_adr(
            title="Persistent ADR",
            context="Test",
            decision="Test",
            consequences="Test",
            status="accepted"
        )
        
        # Create new repository instance (should load persisted index)
        new_repository = FileMemoryRepository(base_path=temp_memory_dir)
        new_index = new_repository.strategic_index
        
        # Verify data was persisted
        assert goal.key in new_index.find_by_type("goal")
        assert goal.key in new_index.find_by_priority("high")
        assert adr.key in new_index.find_by_type("adr")
        assert adr.key in new_index.find_by_status("accepted")
    
    @pytest.mark.asyncio
    async def test_index_statistics(self, use_case, repository):
        """Test index statistics calculation."""
        # Create various entries
        await use_case.create_strategic_goal(
            goal="Goal 1",
            priority="high"
        )
        await use_case.create_strategic_goal(
            goal="Goal 2",
            priority="medium"
        )
        await use_case.create_adr(
            title="ADR 1",
            context="Test",
            decision="Test",
            consequences="Test",
            status="proposed"
        )
        
        # Get statistics
        stats = repository.strategic_index.get_statistics()
        
        # Verify statistics
        assert stats["total_entries"] == 3
        assert stats["by_type"]["goal"] == 2
        assert stats["by_type"]["adr"] == 1
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["medium"] == 1
        assert stats["by_status"]["active"] == 2
        assert stats["by_status"]["proposed"] == 1
        assert stats["total_tags"] > 0
    
    @pytest.mark.asyncio
    async def test_search_with_multiple_tags(self, use_case, repository):
        """Test searching with multiple tags using index."""
        # Create goals with different tag combinations
        await use_case.create_strategic_goal(
            goal="Backend goal",
            priority="high"
        )
        await use_case.create_strategic_goal(
            goal="Frontend goal",
            priority="medium"
        )
        
        # Search for high priority using tags
        results = await repository.search(
            memory_type=MemoryType.STRATEGIC,
            tags=["high", "strategic"]
        )
        
        # Should find at least the high priority goal
        assert len(results) >= 1
        assert any("Backend goal" in str(r.content) for r in results)
    
    @pytest.mark.asyncio
    async def test_index_with_complex_queries(self, use_case, repository):
        """Test index with complex multi-criteria queries."""
        # Create various strategic memories
        await use_case.create_strategic_goal(
            goal="Performance improvement",
            priority="critical",
            milestones=[{"name": "Phase 1"}]
        )
        await use_case.create_strategic_goal(
            goal="Security enhancement",
            priority="high"
        )
        await use_case.create_adr(
            title="Use microservices",
            context="Scalability needs",
            decision="Adopt microservices",
            consequences="Increased complexity",
            status="accepted"
        )
        
        # Complex search: strategic memories with specific tags
        results = await repository.search(
            memory_type=MemoryType.STRATEGIC,
            tags=["strategic"]
        )
        
        # All goals should have strategic tag
        assert len(results) >= 2
        
        # Search for ADRs specifically
        adr_results = await repository.search(
            memory_type=MemoryType.STRATEGIC,
            tags=["adr"]
        )
        
        assert len(adr_results) >= 1
        assert all(r.has_tag("adr") for r in adr_results)
