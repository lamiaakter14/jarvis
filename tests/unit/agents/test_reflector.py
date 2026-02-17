"""Unit tests for the Reflector Agent."""

from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from jarvis_core.agents.reflector import ReflectorAgent
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.shared.exceptions import DomainException


@pytest.mark.unit
@pytest.mark.asyncio
class TestReflectorAgent:
    """Unit tests for ReflectorAgent."""

    @pytest.fixture
    def mock_memory_repo(self):
        """Create a mock memory repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_task_repo(self):
        """Create a mock task repository."""
        repo = AsyncMock()
        repo.list_all = AsyncMock(return_value=[])
        return repo

    @pytest.fixture
    def reflector_agent(self, mock_memory_repo, mock_task_repo):
        """Create a reflector agent instance."""
        return ReflectorAgent(memory_repo=mock_memory_repo, task_repo=mock_task_repo)

    @pytest.fixture
    def sample_context(self):
        """Create a sample context for testing."""
        return Context(
            date=date.today(),
            current_focus=["Test focus"],
            available_hours=8.0,
            strategic_goals=["Goal 1", "Goal 2"],
        )

    def test_reflector_agent_initialization(self, reflector_agent):
        """Test that reflector agent initializes correctly."""
        assert reflector_agent.agent_type == AgentType.REFLECTOR
        assert reflector_agent.name == "Reflector Agent"
        assert "alignment" in reflector_agent.description.lower()

    async def test_execute_with_no_tasks(self, reflector_agent, sample_context, mock_task_repo):
        """Test execution when there are no tasks."""
        mock_task_repo.list_all.return_value = []

        result = await reflector_agent.execute(sample_context)

        assert "reflection_summary" in result
        assert "correction_actions" in result
        assert "pattern_flags" in result
        assert "skill_graph_updates" in result
        assert len(result["correction_actions"]) == 3

    async def test_execute_with_completed_tasks(
        self, reflector_agent, sample_context, mock_task_repo
    ):
        """Test execution with completed tasks."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create mock completed tasks
        completed_task = MagicMock(spec=Task)
        completed_task.status = "completed"
        completed_task.completed_at = datetime.combine(yesterday, datetime.min.time())
        completed_task.tags = ["strategic", "important"]
        completed_task.task_id = "task_1"

        mock_task_repo.list_all.return_value = [completed_task]

        result = await reflector_agent.execute(sample_context)

        assert result["reflection_summary"]
        assert len(result["correction_actions"]) == 3
        assert result["execution_time"] > 0

    async def test_execute_with_missed_tasks(self, reflector_agent, sample_context, mock_task_repo):
        """Test execution with missed tasks."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create mock missed tasks
        missed_task = MagicMock(spec=Task)
        missed_task.status = "pending"
        missed_task.due_date = yesterday
        missed_task.task_id = "task_1"
        missed_task.tags = []

        mock_task_repo.list_all.return_value = [missed_task]

        result = await reflector_agent.execute(sample_context)

        assert result["reflection_summary"]
        # Should flag low completion rate
        assert any(flag["type"] == "low_completion" for flag in result["pattern_flags"])

    async def test_detect_low_completion_pattern(
        self, reflector_agent, sample_context, mock_task_repo
    ):
        """Test detection of low completion rate pattern."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create 1 completed and 4 missed tasks
        completed_task = MagicMock(spec=Task)
        completed_task.status = "completed"
        completed_task.completed_at = datetime.combine(yesterday, datetime.min.time())
        completed_task.tags = []
        completed_task.task_id = "task_1"

        missed_tasks = []
        for i in range(4):
            missed_task = MagicMock(spec=Task)
            missed_task.status = "pending"
            missed_task.due_date = yesterday
            missed_task.task_id = f"task_{i+2}"
            missed_task.tags = []
            missed_tasks.append(missed_task)

        mock_task_repo.list_all.return_value = [completed_task] + missed_tasks

        result = await reflector_agent.execute(sample_context)

        # Should detect low completion and task accumulation
        pattern_types = [flag["type"] for flag in result["pattern_flags"]]
        assert "low_completion" in pattern_types
        assert "task_accumulation" in pattern_types

    async def test_detect_strategic_misalignment(
        self, reflector_agent, sample_context, mock_task_repo
    ):
        """Test detection of strategic misalignment."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create completed tasks without strategic tags
        tasks = []
        for i in range(5):
            task = MagicMock(spec=Task)
            task.status = "completed"
            task.completed_at = datetime.combine(yesterday, datetime.min.time())
            task.tags = ["regular"]  # No strategic tags
            task.task_id = f"task_{i+1}"
            tasks.append(task)

        mock_task_repo.list_all.return_value = tasks

        result = await reflector_agent.execute(sample_context)

        # Should detect strategic misalignment
        pattern_types = [flag["type"] for flag in result["pattern_flags"]]
        assert "strategic_misalignment" in pattern_types

    async def test_correction_actions_count(self, reflector_agent, sample_context, mock_task_repo):
        """Test that exactly 3 correction actions are returned."""
        mock_task_repo.list_all.return_value = []

        result = await reflector_agent.execute(sample_context)

        assert len(result["correction_actions"]) == 3
        # Check that actions have required fields
        for action in result["correction_actions"]:
            assert "priority" in action
            assert "action_type" in action
            assert "title" in action
            assert "description" in action
            assert "expected_impact" in action
            assert "effort" in action

    async def test_correction_actions_prioritized(
        self, reflector_agent, sample_context, mock_task_repo
    ):
        """Test that correction actions are prioritized correctly."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create scenario with multiple issues
        completed_task = MagicMock(spec=Task)
        completed_task.status = "completed"
        completed_task.completed_at = datetime.combine(yesterday, datetime.min.time())
        completed_task.tags = []
        completed_task.task_id = "task_1"

        missed_tasks = []
        for i in range(5):
            missed_task = MagicMock(spec=Task)
            missed_task.status = "pending"
            missed_task.due_date = yesterday
            missed_task.task_id = f"task_{i+2}"
            missed_task.tags = []
            missed_tasks.append(missed_task)

        mock_task_repo.list_all.return_value = [completed_task] + missed_tasks

        result = await reflector_agent.execute(sample_context)

        actions = result["correction_actions"]
        # Check that priority 1 actions come first
        priorities = [action["priority"] for action in actions]
        assert priorities == sorted(priorities)

    async def test_skill_graph_updates(self, reflector_agent, sample_context, mock_task_repo):
        """Test that skill graph updates are generated."""
        yesterday = sample_context.date - timedelta(days=1)

        # Create tasks with low completion rate
        completed_task = MagicMock(spec=Task)
        completed_task.status = "completed"
        completed_task.completed_at = datetime.combine(yesterday, datetime.min.time())
        completed_task.tags = []
        completed_task.task_id = "task_1"

        missed_tasks = []
        for i in range(3):
            missed_task = MagicMock(spec=Task)
            missed_task.status = "pending"
            missed_task.due_date = yesterday
            missed_task.task_id = f"task_{i+2}"
            missed_task.tags = []
            missed_tasks.append(missed_task)

        mock_task_repo.list_all.return_value = [completed_task] + missed_tasks

        result = await reflector_agent.execute(sample_context)

        # Should suggest skill updates
        assert len(result["skill_graph_updates"]) > 0
        for update in result["skill_graph_updates"]:
            assert "skill_pattern" in update
            assert "suggested_weight" in update
            assert "reason" in update

    async def test_reflection_stored_in_memory(
        self, reflector_agent, sample_context, mock_memory_repo, mock_task_repo
    ):
        """Test that reflection is stored in memory."""
        mock_task_repo.list_all.return_value = []

        await reflector_agent.execute(sample_context)

        # Verify that memory was saved
        assert mock_memory_repo.save.called
        saved_memory = mock_memory_repo.save.call_args[0][0]
        assert saved_memory.type.value == "execution_log"
        assert "reflection" in saved_memory.get_tags()

    async def test_execution_metrics_tracked(self, reflector_agent, sample_context, mock_task_repo):
        """Test that execution metrics are tracked."""
        mock_task_repo.list_all.return_value = []

        initial_executions = reflector_agent.total_executions

        await reflector_agent.execute(sample_context)

        assert reflector_agent.total_executions == initial_executions + 1
        assert reflector_agent.successful_executions > 0
        assert reflector_agent.last_execution_time is not None

    async def test_execute_handles_repository_error(
        self, reflector_agent, sample_context, mock_task_repo
    ):
        """Test that execute handles repository errors gracefully."""
        mock_task_repo.list_all.side_effect = Exception("Repository error")

        with pytest.raises(DomainException) as exc_info:
            await reflector_agent.execute(sample_context)

        assert "Reflector execution failed" in str(exc_info.value)
        assert reflector_agent.failed_executions > 0

    async def test_reflection_summary_format(self, reflector_agent, sample_context, mock_task_repo):
        """Test that reflection summary has proper format."""
        mock_task_repo.list_all.return_value = []

        result = await reflector_agent.execute(sample_context)

        summary = result["reflection_summary"]
        assert "# Daily Reflection" in summary
        assert "## Execution Performance" in summary
        assert "## Drift Analysis" in summary
        assert "## Recommended Corrections" in summary

    async def test_drift_level_calculation(self, reflector_agent, sample_context, mock_task_repo):
        """Test drift level calculation based on patterns."""
        # Test with no issues - should have minimal drift
        mock_task_repo.list_all.return_value = []
        result = await reflector_agent.execute(sample_context)

        # With no tasks, should have default recommendations
        assert result["correction_actions"]

        # Test with multiple issues - should have higher drift
        yesterday = sample_context.date - timedelta(days=1)
        completed_task = MagicMock(spec=Task)
        completed_task.status = "completed"
        completed_task.completed_at = datetime.combine(yesterday, datetime.min.time())
        completed_task.tags = []
        completed_task.task_id = "task_1"

        missed_tasks = []
        for i in range(6):
            missed_task = MagicMock(spec=Task)
            missed_task.status = "pending"
            missed_task.due_date = yesterday
            missed_task.task_id = f"task_{i+2}"
            missed_task.tags = []
            missed_tasks.append(missed_task)

        mock_task_repo.list_all.return_value = [completed_task] + missed_tasks

        result = await reflector_agent.execute(sample_context)
        assert len(result["pattern_flags"]) > 1
