"""V2 Cognitive Loop endpoint."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from jarvis_core.orchestrator.loop import CognitiveOrchestrator, CognitiveLoopResult
from jarvis_core.orchestrator.context import CognitiveContext, CognitiveProfile
from jarvis_core.cognition.models import EnergyModel, IdentityModel, DecisionProfile
from jarvis_core.shared.exceptions import DomainException

router = APIRouter()


class CognitiveLoopRequest(BaseModel):
    """Request model for cognitive loop execution.
    
    Attributes:
        energy_model: Optional energy model configuration
        identity_model: Optional identity model configuration
        decision_profile: Optional decision profile configuration
    """
    
    energy_model: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Energy model with sleep hours, energy score, etc."
    )
    identity_model: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Identity model with mission and goals"
    )
    decision_profile: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Decision profile with speed/accuracy bias"
    )


class CognitiveLoopResponse(BaseModel):
    """Response model for cognitive loop execution.
    
    Attributes:
        plan: Daily plan with tasks
        knowledge_gaps: Identified knowledge gaps
        innovations: Innovation suggestions
        reflection: Reflection analysis
        metrics: Performance metrics
    """
    
    plan: Dict[str, Any] = Field(..., description="Daily plan from strategist")
    knowledge_gaps: list = Field(..., description="Identified knowledge gaps")
    innovations: list = Field(..., description="Innovation suggestions")
    reflection: Dict[str, Any] = Field(..., description="Reflection analysis")
    metrics: Dict[str, Any] = Field(..., description="Performance metrics")


def get_orchestrator() -> CognitiveOrchestrator:
    """Dependency to get orchestrator instance.
    
    This is a placeholder. In production, this would use proper dependency injection
    from the config/dependencies module.
    
    Returns:
        CognitiveOrchestrator instance
    """
    from jarvis_core.infrastructure.agents.strategist_agent import StrategistAgent
    from jarvis_core.infrastructure.agents.executor_agent import ExecutorAgent
    from jarvis_core.infrastructure.agents.innovator_agent import InnovatorAgent
    from jarvis_core.infrastructure.agents.amplifier_agent import AmplifierAgent
    from jarvis_core.agents.reflector import ReflectorAgent
    from jarvis_core.cognition.service import CognitiveService
    from jarvis_core.metrics.engine import MetricsEngine
    from jarvis_core.infrastructure.persistence.json_storage import JsonStorage
    from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
    from jarvis_core.infrastructure.persistence.sqlite_task_repository import SQLiteTaskRepository
    from jarvis_core.infrastructure.ai.openai_service import OpenAIService
    from jarvis_core.infrastructure.monitoring.metrics_collector import MetricsCollector
    
    # Initialize repositories
    memory_repo = FileMemoryRepository(storage=JsonStorage())
    task_repo = SQLiteTaskRepository(db_path=":memory:")
    ai_service = OpenAIService()
    metrics_collector = MetricsCollector()
    
    # Initialize agents
    strategist = StrategistAgent(
        ai_service=ai_service,
        memory_repo=memory_repo,
        task_repo=task_repo
    )
    
    executor = ExecutorAgent(
        task_repo=task_repo
    )
    
    innovator = InnovatorAgent(
        ai_service=ai_service,
        memory_repo=memory_repo
    )
    
    amplifier = AmplifierAgent(
        memory_repo=memory_repo,
        metrics_collector=metrics_collector
    )
    
    reflector = ReflectorAgent(
        memory_repo=memory_repo,
        task_repo=task_repo
    )
    
    # Initialize services
    cognitive_service = CognitiveService()
    metrics_engine = MetricsEngine()
    
    return CognitiveOrchestrator(
        strategist_agent=strategist,
        executor_agent=executor,
        innovator_agent=innovator,
        amplifier_agent=amplifier,
        reflector_agent=reflector,
        cognitive_service=cognitive_service,
        metrics_engine=metrics_engine,
        task_repository=task_repo,
        memory_repository=memory_repo
    )


@router.post("/cognitive-loop/run", response_model=CognitiveLoopResponse)
async def run_cognitive_loop(
    request: CognitiveLoopRequest = None,
    orchestrator: CognitiveOrchestrator = Depends(get_orchestrator)
) -> CognitiveLoopResponse:
    """Execute the complete cognitive loop with all agents.
    
    This endpoint orchestrates the execution of:
    1. STRATEGIST - Creates daily plan
    2. EXECUTOR - Executes tasks
    3. INNOVATOR - Generates innovations
    4. AMPLIFIER - Collects performance metrics
    5. REFLECTOR - Analyzes and suggests corrections
    
    Args:
        request: Optional request with cognitive models
        orchestrator: Cognitive orchestrator dependency
        
    Returns:
        CognitiveLoopResponse with all results
        
    Raises:
        HTTPException: If cognitive loop execution fails
    """
    try:
        # Create cognitive context from request
        context = CognitiveContext.create_default()
        
        if request:
            # Update profile from request
            if request.energy_model:
                context.profile.energy = EnergyModel(**request.energy_model)
            
            if request.identity_model:
                context.profile.identity = IdentityModel(**request.identity_model)
            
            if request.decision_profile:
                context.profile.decision = DecisionProfile(**request.decision_profile)
        
        # Execute cognitive loop
        result = await orchestrator.run(cognitive_context=context)
        
        # Return formatted response
        return CognitiveLoopResponse(
            plan=result.plan,
            knowledge_gaps=result.knowledge_gaps,
            innovations=result.innovations,
            reflection=result.reflection,
            metrics=result.metrics
        )
    
    except DomainException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cognitive loop execution failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/cognitive-loop/health")
async def cognitive_loop_health():
    """Health check for cognitive loop endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "version": "2.0",
        "endpoint": "/v2/cognitive-loop/run"
    }
