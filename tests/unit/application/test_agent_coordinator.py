"""Tests for agent coordinator service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from jarvis_core.application.services.agent_coordinator import AgentCoordinator
from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.task import Task
from jarvis_core.shared.constants import AgentType, TaskStatus, TaskPriority


class MockAgent(Agent):
    """Mock agent for testing."""
    
    def __init__(self, agent_type: AgentType):
        super().__init__(
            agent_id=f"agent_{agent_type.value}",
            agent_type=agent_type,
            name=f"{agent_type.value} Agent"
        )
        self.execution_count = 0
        self.should_fail = False
    
    async def execute(self, context: Context):
        """Mock execute method."""
        self.execution_count += 1
        if self.should_fail:
            raise Exception("Mock execution failed")
        return {"status": "success", "agent": self.name}


@pytest.mark.unit
class TestAgentCoordinator:
    """Unit tests for agent coordinator service."""
    
    @pytest.fixture
    def mock_task_repository(self):
        """Create mock task repository."""
        return AsyncMock()
    
    @pytest.fixture
    def coordinator(self, mock_task_repository):
        """Create agent coordinator."""
        return AgentCoordinator(mock_task_repository)
    
    @pytest.fixture
    def context(self):
        """Create test context."""
        return Context(
            available_hours=8.0,
            current_focus=["Testing"]
        )
    
    def test_register_agent(self, coordinator):
        """Test agent registration."""
        agent = MockAgent(AgentType.STRATEGIST)
        coordinator.register_agent(agent)
        
        retrieved = coordinator.get_agent(AgentType.STRATEGIST)
        assert retrieved == agent
    
    def test_get_unregistered_agent(self, coordinator):
        """Test getting unregistered agent returns None."""
        agent = coordinator.get_agent(AgentType.EXECUTOR)
        assert agent is None
    
    @pytest.mark.asyncio
    async def test_coordinate_task_execution_no_tasks(
        self, coordinator, context, mock_task_repository
    ):
        """Test coordination when no pending tasks exist."""
        mock_task_repository.list.return_value = []
        
        result = await coordinator.coordinate_task_execution(context)
        
        assert result["status"] == "no_tasks"
        assert result["executed"] == 0
    
    @pytest.mark.asyncio
    async def test_coordinate_task_execution_success(
        self, coordinator, context, mock_task_repository
    ):
        """Test successful task coordination."""
        # Register agent
        agent = MockAgent(AgentType.EXECUTOR)
        coordinator.register_agent(agent)
        
        # Create test tasks
        task = Task(
            task_id="task_001",
            title="Test Task",
            agent_type=AgentType.EXECUTOR,
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING
        )
        mock_task_repository.list.return_value = [task]
        
        result = await coordinator.coordinate_task_execution(context)
        
        assert result["total_tasks"] == 1
        assert result["executed"] == 1
        assert result["failed"] == 0
        assert mock_task_repository.save.call_count >= 2  # Initial and completion
    
    @pytest.mark.asyncio
    async def test_coordinate_task_execution_agent_not_found(
        self, coordinator, context, mock_task_repository
    ):
        """Test coordination when agent is not registered."""
        # Create task without registered agent
        task = Task(
            task_id="task_002",
            title="Test Task",
            agent_type=AgentType.INNOVATOR,
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING
        )
        mock_task_repository.list.return_value = [task]
        
        result = await coordinator.coordinate_task_execution(context)
        
        assert result["total_tasks"] == 1
        assert result["skipped"] == 1
        assert result["executed"] == 0
    
    @pytest.mark.asyncio
    async def test_coordinate_task_execution_with_failure(
        self, coordinator, context, mock_task_repository
    ):
        """Test coordination when agent execution fails."""
        # Register failing agent
        agent = MockAgent(AgentType.EXECUTOR)
        agent.should_fail = True
        coordinator.register_agent(agent)
        
        # Create test task
        task = Task(
            task_id="task_003",
            title="Test Task",
            agent_type=AgentType.EXECUTOR,
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING
        )
        mock_task_repository.list.return_value = [task]
        
        result = await coordinator.coordinate_task_execution(context)
        
        assert result["total_tasks"] == 1
        assert result["executed"] == 0
        assert result["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_coordinate_task_execution_priority_order(
        self, coordinator, context, mock_task_repository
    ):
        """Test tasks are executed in priority order."""
        # Register agent
        agent = MockAgent(AgentType.EXECUTOR)
        coordinator.register_agent(agent)
        
        # Create tasks with different priorities
        tasks = [
            Task(
                task_id="task_low",
                title="Low Priority",
                agent_type=AgentType.EXECUTOR,
                priority=TaskPriority.LOW,
                status=TaskStatus.PENDING
            ),
            Task(
                task_id="task_critical",
                title="Critical Priority",
                agent_type=AgentType.EXECUTOR,
                priority=TaskPriority.CRITICAL,
                status=TaskStatus.PENDING
            ),
            Task(
                task_id="task_medium",
                title="Medium Priority",
                agent_type=AgentType.EXECUTOR,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING
            ),
            Task(
                task_id="task_high",
                title="High Priority",
                agent_type=AgentType.EXECUTOR,
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING
            ),
        ]
        mock_task_repository.list.return_value = tasks
        
        result = await coordinator.coordinate_task_execution(context)
        
        # Verify all tasks were executed
        assert result["executed"] == 4
        
        # Verify critical task was executed first
        assert result["task_results"][0]["task_id"] == "task_critical"
    
    @pytest.mark.asyncio
    async def test_coordinate_agents_parallel(
        self, coordinator, context
    ):
        """Test parallel agent execution."""
        # Register multiple agents
        strategist = MockAgent(AgentType.STRATEGIST)
        executor = MockAgent(AgentType.EXECUTOR)
        mentor = MockAgent(AgentType.MENTOR)
        
        coordinator.register_agent(strategist)
        coordinator.register_agent(executor)
        coordinator.register_agent(mentor)
        
        agent_types = [
            AgentType.STRATEGIST,
            AgentType.EXECUTOR,
            AgentType.MENTOR
        ]
        
        result = await coordinator.coordinate_agents_parallel(
            context,
            agent_types,
            max_concurrent=2
        )
        
        assert result["total_agents"] == 3
        assert result["successful"] == 3
        assert result["failed"] == 0
        
        # Verify all agents were executed
        assert strategist.execution_count == 1
        assert executor.execution_count == 1
        assert mentor.execution_count == 1
    
    @pytest.mark.asyncio
    async def test_coordinate_agents_parallel_with_failure(
        self, coordinator, context
    ):
        """Test parallel agent execution with failures."""
        # Register agents with one failing
        strategist = MockAgent(AgentType.STRATEGIST)
        executor = MockAgent(AgentType.EXECUTOR)
        executor.should_fail = True
        
        coordinator.register_agent(strategist)
        coordinator.register_agent(executor)
        
        agent_types = [AgentType.STRATEGIST, AgentType.EXECUTOR]
        
        result = await coordinator.coordinate_agents_parallel(
            context,
            agent_types
        )
        
        assert result["total_agents"] == 2
        assert result["successful"] == 1
        assert result["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_synchronize_strategic_agents(
        self, coordinator, context
    ):
        """Test synchronized strategic agent execution."""
        # Register strategic agents
        strategist = MockAgent(AgentType.STRATEGIST)
        executor = MockAgent(AgentType.EXECUTOR)
        mentor = MockAgent(AgentType.MENTOR)
        
        coordinator.register_agent(strategist)
        coordinator.register_agent(executor)
        coordinator.register_agent(mentor)
        
        result = await coordinator.synchronize_strategic_agents(context)
        
        assert result["workflow"] == "strategic_agents_sync"
        assert len(result["steps"]) == 3
        assert result["overall_status"] == "success"
        
        # Verify execution order
        assert result["steps"][0]["agent"] == "STRATEGIST"
        assert result["steps"][1]["agent"] == "EXECUTOR"
        assert result["steps"][2]["agent"] == "MENTOR"
    
    @pytest.mark.asyncio
    async def test_synchronize_strategic_agents_with_failure(
        self, coordinator, context
    ):
        """Test synchronized execution with agent failure."""
        # Register agents with one failing
        strategist = MockAgent(AgentType.STRATEGIST)
        executor = MockAgent(AgentType.EXECUTOR)
        executor.should_fail = True
        mentor = MockAgent(AgentType.MENTOR)
        
        coordinator.register_agent(strategist)
        coordinator.register_agent(executor)
        coordinator.register_agent(mentor)
        
        result = await coordinator.synchronize_strategic_agents(context)
        
        assert result["overall_status"] == "partial_failure"
        assert len(result["steps"]) == 3
        
        # Verify strategist and mentor succeeded
        assert result["steps"][0]["status"] == "success"
        assert result["steps"][1]["status"] == "failed"
        assert result["steps"][2]["status"] == "success"
