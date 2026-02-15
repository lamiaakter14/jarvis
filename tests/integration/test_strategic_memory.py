"""Integration tests for strategic memory management."""

import pytest
from datetime import datetime
import tempfile
import shutil

from jarvis_core.application.use_cases.manage_strategic_memory import ManageStrategicMemory
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
from jarvis_core.shared.constants import MemoryType


@pytest.mark.integration
class TestManageStrategicMemory:
    """Integration tests for ManageStrategicMemory use case."""
    
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
    async def test_create_strategic_goal(self, use_case):
        """Test creating a strategic goal."""
        goal = await use_case.create_strategic_goal(
            goal="Complete project milestone",
            description="Finish phase 1 of the project",
            priority="high",
            milestones=[
                {"name": "Design", "status": "completed"},
                {"name": "Implementation", "status": "in_progress"}
            ]
        )
        
        assert goal is not None
        assert goal.type == MemoryType.STRATEGIC
        assert goal.content["goal"] == "Complete project milestone"
        assert goal.content["priority"] == "high"
        assert len(goal.content["milestones"]) == 2
        assert goal.has_tag("strategic")
        assert goal.has_tag("high")
    
    @pytest.mark.asyncio
    async def test_update_goal_progress(self, use_case):
        """Test updating goal progress."""
        # Create a goal
        goal = await use_case.create_strategic_goal(
            goal="Test Goal",
            priority="medium"
        )
        
        # Update progress
        updated_goal = await use_case.update_goal_progress(
            goal_key=goal.key,
            progress=50.0,
            status="active"
        )
        
        assert updated_goal.content["progress"] == 50.0
        assert updated_goal.content["status"] == "active"
        assert updated_goal.get_version() == 2  # Version incremented
    
    @pytest.mark.asyncio
    async def test_list_active_goals(self, use_case):
        """Test listing active goals."""
        # Create multiple goals
        await use_case.create_strategic_goal(
            goal="Goal 1",
            priority="critical"
        )
        await use_case.create_strategic_goal(
            goal="Goal 2",
            priority="high"
        )
        
        # Create a completed goal
        completed_goal = await use_case.create_strategic_goal(
            goal="Goal 3",
            priority="medium"
        )
        await use_case.update_goal_progress(
            goal_key=completed_goal.key,
            progress=100.0,
            status="completed"
        )
        
        # List active goals
        active_goals = await use_case.list_active_goals()
        
        assert len(active_goals) == 2
        assert all(g.content["status"] == "active" for g in active_goals)
        # Check priority ordering (critical first)
        assert active_goals[0].content["priority"] == "critical"
        assert active_goals[1].content["priority"] == "high"
    
    @pytest.mark.asyncio
    async def test_create_adr(self, use_case):
        """Test creating an Architecture Decision Record."""
        adr = await use_case.create_adr(
            title="Use PostgreSQL for database",
            context="We need a reliable relational database",
            decision="We will use PostgreSQL",
            consequences="Strong ACID compliance, good performance",
            status="accepted",
            alternatives=["MySQL", "MongoDB"]
        )
        
        assert adr is not None
        assert adr.type == MemoryType.STRATEGIC
        assert adr.content["title"] == "Use PostgreSQL for database"
        assert adr.content["status"] == "accepted"
        assert len(adr.content["alternatives"]) == 2
        assert adr.has_tag("adr")
        assert adr.has_tag("architecture")
    
    @pytest.mark.asyncio
    async def test_list_adrs(self, use_case):
        """Test listing ADRs."""
        # Create multiple ADRs
        await use_case.create_adr(
            title="ADR 1",
            context="Context 1",
            decision="Decision 1",
            consequences="Consequences 1",
            status="proposed"
        )
        await use_case.create_adr(
            title="ADR 2",
            context="Context 2",
            decision="Decision 2",
            consequences="Consequences 2",
            status="accepted"
        )
        await use_case.create_adr(
            title="ADR 3",
            context="Context 3",
            decision="Decision 3",
            consequences="Consequences 3",
            status="accepted"
        )
        
        # List all ADRs
        all_adrs = await use_case.list_adrs()
        assert len(all_adrs) == 3
        
        # List only accepted ADRs
        accepted_adrs = await use_case.list_adrs(status="accepted")
        assert len(accepted_adrs) == 2
        assert all(adr.content["status"] == "accepted" for adr in accepted_adrs)
    
    @pytest.mark.asyncio
    async def test_search_strategic_memory(self, use_case):
        """Test searching strategic memory."""
        # Create goals with different keywords
        await use_case.create_strategic_goal(
            goal="Improve system performance",
            description="Optimize database queries",
            priority="high"
        )
        await use_case.create_strategic_goal(
            goal="Enhance user experience",
            description="Redesign UI",
            priority="medium"
        )
        
        # Search by keyword
        results = await use_case.search_strategic_memory(
            keywords=["performance"]
        )
        
        assert len(results) >= 1
        assert any("performance" in str(r.content).lower() for r in results)
    
    @pytest.mark.asyncio
    async def test_search_by_tags(self, use_case):
        """Test searching strategic memory by tags."""
        # Create goals
        await use_case.create_strategic_goal(
            goal="High priority goal",
            priority="high"
        )
        await use_case.create_strategic_goal(
            goal="Medium priority goal",
            priority="medium"
        )
        
        # Search for high priority goals
        results = await use_case.search_strategic_memory(
            tags=["high"]
        )
        
        assert len(results) >= 1
        assert all(r.has_tag("high") for r in results)
    
    @pytest.mark.asyncio
    async def test_goal_with_dependencies(self, use_case):
        """Test creating goal with dependencies."""
        # Create a prerequisite goal
        prereq_goal = await use_case.create_strategic_goal(
            goal="Setup infrastructure",
            priority="high"
        )
        
        # Create a dependent goal
        dependent_goal = await use_case.create_strategic_goal(
            goal="Deploy application",
            priority="high",
            dependencies=[prereq_goal.key]
        )
        
        assert prereq_goal.key in dependent_goal.content["dependencies"]
    
    @pytest.mark.asyncio
    async def test_goal_with_metrics(self, use_case):
        """Test creating goal with success metrics."""
        goal = await use_case.create_strategic_goal(
            goal="Increase performance",
            priority="high",
            metrics={
                "response_time": {"target": "< 200ms", "current": "350ms"},
                "throughput": {"target": "1000 req/s", "current": "600 req/s"}
            }
        )
        
        assert "response_time" in goal.content["metrics"]
        assert "throughput" in goal.content["metrics"]
        assert goal.content["metrics"]["response_time"]["target"] == "< 200ms"
