"""Unit tests for Cognitive Orchestrator."""

import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from jarvis_core.orchestrator.loop import CognitiveOrchestrator, CognitiveLoopResult
from jarvis_core.orchestrator.context import CognitiveContext, CognitiveProfile
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.plan import Plan
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.cognition.models import EnergyModel, IdentityModel
from jarvis_core.shared.exceptions import DomainException


@pytest.mark.unit
@pytest.mark.asyncio
class TestCognitiveOrchestrator:
    """Unit tests for CognitiveOrchestrator."""

    @pytest.fixture
    def mock_strategist(self):
        """Create mock strategist agent."""
        agent = AsyncMock()
        plan = MagicMock(spec=Plan)
        plan.plan_id = "plan_1"
        plan.tasks = []
        agent.execute.return_value = plan
        return agent

    @pytest.fixture
    def mock_executor(self):
        """Create mock executor agent."""
        agent = AsyncMock()
        agent.execute.return_value = {"status": "completed"}
        return agent

    @pytest.fixture
    def mock_innovator(self):
        """Create mock innovator agent."""
        agent = AsyncMock()
        innovation = MagicMock(spec=Innovation)
        innovation.title = "Test Innovation"
        innovation.description = "Test description"
        innovation.impact_score = 0.8
        innovation.category = "automation"
        agent.execute.return_value = [innovation]
        return agent

    @pytest.fixture
    def mock_amplifier(self):
        """Create mock amplifier agent."""
        agent = AsyncMock()
        agent.execute.return_value = {
            "productivity_score": 0.85,
            "optimization_suggestions": ["Optimize morning routine"],
            "performance_trends": {"last_week": 0.8}
        }
        return agent

    @pytest.fixture
    def mock_reflector(self):
        """Create mock reflector agent."""
        agent = AsyncMock()
        agent.execute.return_value = {
            "reflection_summary": "Test summary",
            "correction_actions": [
                {"priority": 1, "title": "Action 1"}
            ],
            "pattern_flags": [],
            "skill_graph_updates": [],
            "drift_level": "none"
        }
        return agent

    @pytest.fixture
    def mock_cognitive_service(self):
        """Create mock cognitive service."""
        service = MagicMock()
        service.update_energy.return_value = {
            "optimal_focus_hours": 6.0,
            "adjusted_energy_score": 0.9
        }
        return service

    @pytest.fixture
    def mock_metrics_engine(self):
        """Create mock metrics engine."""
        engine = MagicMock()
        metrics_report = MagicMock()
        metrics_report.strategic_alignment_score = 0.8
        metrics_report.cognitive_throughput = 1.5
        metrics_report.learning_velocity = 0.2
        metrics_report.momentum_index = 0.75
        engine.calculate_metrics.return_value = metrics_report
        return engine

    @pytest.fixture
    def mock_task_repo(self):
        """Create mock task repository."""
        repo = AsyncMock()
        repo.list_all.return_value = []
        return repo

    @pytest.fixture
    def mock_memory_repo(self):
        """Create mock memory repository."""
        return AsyncMock()

    @pytest.fixture
    def orchestrator(
        self,
        mock_strategist,
        mock_executor,
        mock_innovator,
        mock_amplifier,
        mock_reflector,
        mock_cognitive_service,
        mock_metrics_engine,
        mock_task_repo,
        mock_memory_repo
    ):
        """Create cognitive orchestrator instance."""
        return CognitiveOrchestrator(
            strategist_agent=mock_strategist,
            executor_agent=mock_executor,
            innovator_agent=mock_innovator,
            amplifier_agent=mock_amplifier,
            reflector_agent=mock_reflector,
            cognitive_service=mock_cognitive_service,
            metrics_engine=mock_metrics_engine,
            task_repository=mock_task_repo,
            memory_repository=mock_memory_repo
        )

    async def test_orchestrator_run_with_default_context(self, orchestrator):
        """Test orchestrator runs successfully with default context."""
        result = await orchestrator.run()

        assert isinstance(result, CognitiveLoopResult)
        assert "plan" in result.to_dict()
        assert "knowledge_gaps" in result.to_dict()
        assert "innovations" in result.to_dict()
        assert "reflection" in result.to_dict()
        assert "metrics" in result.to_dict()
        assert result.execution_time > 0

    async def test_orchestrator_run_with_custom_context(self, orchestrator):
        """Test orchestrator runs with custom cognitive context."""
        custom_context = CognitiveContext.create_default(execution_date=date(2024, 1, 1))
        custom_context.profile.identity.current_primary_mission = "Test mission"

        result = await orchestrator.run(cognitive_context=custom_context)

        assert isinstance(result, CognitiveLoopResult)
        assert result.execution_time > 0

    async def test_all_agents_called(
        self, orchestrator, mock_strategist, mock_executor,
        mock_innovator, mock_amplifier, mock_reflector
    ):
        """Test that all agents are called during execution."""
        await orchestrator.run()

        assert mock_strategist.execute.called
        # Executor is only called if there are pending tasks
        # assert mock_executor.execute.called
        assert mock_innovator.execute.called
        assert mock_amplifier.execute.called
        assert mock_reflector.execute.called

    async def test_cognitive_service_updates_energy(
        self, orchestrator, mock_cognitive_service
    ):
        """Test that cognitive service updates energy model."""
        await orchestrator.run()

        assert mock_cognitive_service.update_energy.called

    async def test_results_persisted_to_memory(
        self, orchestrator, mock_memory_repo
    ):
        """Test that results are persisted to memory."""
        await orchestrator.run()

        assert mock_memory_repo.save.called
        saved_memory = mock_memory_repo.save.call_args[0][0]
        assert "cognitive_loop" in saved_memory.get_tags()

    async def test_result_contains_all_required_fields(self, orchestrator):
        """Test that result contains all required fields."""
        result = await orchestrator.run()

        result_dict = result.to_dict()
        assert "plan" in result_dict
        assert "knowledge_gaps" in result_dict
        assert "innovations" in result_dict
        assert "reflection" in result_dict
        assert "metrics" in result_dict
        assert "execution_time" in result_dict
        assert "timestamp" in result_dict

    async def test_orchestrator_handles_agent_failure(
        self, orchestrator, mock_strategist
    ):
        """Test that orchestrator handles agent failure gracefully."""
        mock_strategist.execute.side_effect = Exception("Agent failed")

        with pytest.raises(DomainException) as exc_info:
            await orchestrator.run()

        assert "Cognitive loop execution failed" in str(exc_info.value)
