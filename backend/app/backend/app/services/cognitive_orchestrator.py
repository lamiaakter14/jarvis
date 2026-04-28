"""
JARVIS Cognitive Orchestrator
Phase 4: Perceive → Reason → Act → Reflect Pipeline
"""
from typing import Dict, Any
from app.agents.strategist_agent import StrategistAgent
from app.agents.amplifier_agent import AmplifierAgent
from app.agents.reflector_agent import ReflectorAgent
from app.memory.memory_service import MemoryService

class CognitiveOrchestrator:
    """Orchestrates the cognitive loop with 3 agents + memory"""
    
    def __init__(self):
        self.strategist = StrategistAgent()
        self.amplifier = AmplifierAgent()
        self.reflector = ReflectorAgent()
        self.memory = MemoryService()
    
    async def process_task(self, task: Dict) -> Dict:
        """Phase 4: Full cognitive pipeline for task processing"""
        
        # Step 1: PERCEIVE - Get memory context
        context = self.memory.get_context(query=task.get("title"))
        
        # Step 2: REASON - Strategist analyzes
        analysis = await self.strategist.analyze_task(task)
        self.memory.store_episode("task_analyzed", {"task": task, "analysis": analysis})
        
        # Step 3: ACT - Amplifier enhances
        amplified = await self.amplifier.amplify()
        self.memory.store_knowledge(f"task_{task['id']}_approach", amplified)
        
        # Step 4: REFLECT - Reflector validates
        reflection = await self.reflector.reflect_on_task(task, analysis)
        self.memory.store_strategy("task_pattern", {"analysis": analysis, "reflection": reflection})
        
        return {
            "task_id": task.get("id"),
            "pipeline": ["perceive", "reason", "act", "reflect"],
            "context": context,
            "analysis": analysis,
            "amplified_insight": amplified,
            "reflection": reflection,
            "memory_stored": True,
            "phase": "4-orchestration"
        }
    
    async def perceive_environment(self, perception_type: str) -> Dict:
        """Context-aware perception routing"""
        
        result = None
        agent_used = None
        
        if perception_type in ["context", "recommendation"]:
            result = await self.strategist.perceive_context()
            agent_used = "strategist"
        elif perception_type in ["aether", "stats"]:
            result = await self.amplifier.amplify()
            agent_used = "amplifier"
        
        # Store in episodic memory
        self.memory.store_episode("perception", {
            "type": perception_type,
            "agent": agent_used,
            "result": result
        })
        
        return {
            "perception_type": perception_type,
            "agent": agent_used,
            "result": result,
            "phase": "4-orchestration"
        }
    
    def get_memory_stats(self) -> Dict:
        """Get memory system statistics"""
        return {
            "episodic_count": len(self.memory.episodic),
            "semantic_keys": list(self.memory.semantic.keys()),
            "strategic_count": len(self.memory.strategic),
            "phase": "4-orchestration"
        }
