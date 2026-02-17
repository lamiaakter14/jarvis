"""Cognitive loop endpoint."""

from typing import Any

from fastapi import APIRouter, HTTPException

try:
    from jarvis_core.bridge.agent_bridge import (
        AmplifierBridge,
        ExecutorBridge,
        InnovatorBridge,
        MentorBridge,
        StrategistBridge,
    )
except ImportError:
    # Fallback if bridge is not available
    StrategistBridge = None
    MentorBridge = None
    ExecutorBridge = None
    InnovatorBridge = None
    AmplifierBridge = None


router = APIRouter()


@router.post("/cognitive-loop")
async def run_cognitive_loop() -> dict[str, Any]:
    """Execute the complete cognitive loop with all 5 agents."""
    try:
        if not all(
            [StrategistBridge, MentorBridge, ExecutorBridge, InnovatorBridge, AmplifierBridge]
        ):
            raise HTTPException(status_code=503, detail="Agent bridges not available")

        # Initialize agents
        strategist = StrategistBridge()
        mentor = MentorBridge()
        executor = ExecutorBridge()
        innovator = InnovatorBridge()
        amplifier = AmplifierBridge()

        # Execute each agent
        plan = strategist.generate_plan()
        gaps = mentor.analyze_execution_logs()

        # Mentor each task in the plan
        task_feedback = []
        for task in plan.get("tasks", []):
            feedback = mentor.mentor_task(task)
            task_feedback.append(feedback)

        executor.run_tasks()
        innovations = innovator.create_innovations()
        performance = amplifier.amplify()

        return {
            "status": "success",
            "strategist": {"plan": plan},
            "mentor": {"gaps": gaps, "task_feedback": task_feedback},
            "executor": {"status": "completed"},
            "innovator": {"innovations": innovations},
            "amplifier": {"performance": performance},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cognitive loop failed: {str(e)}")
