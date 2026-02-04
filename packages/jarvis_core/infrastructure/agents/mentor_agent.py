"""Mentor agent implementation."""

from typing import Any, Dict, List
import time

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException


class MentorAgent(Agent):
    """Mentor agent for guidance and gap identification.
    
    The mentor analyzes execution logs, identifies knowledge and skill gaps,
    and provides guidance and mentorship for tasks and learning.
    """
    
    def __init__(
        self,
        ai_service: IAIService,
        memory_repo: IMemoryRepository,
    ):
        """Initialize mentor agent.
        
        Args:
            ai_service: AI service for analysis and guidance
            memory_repo: Memory repository for accessing execution logs
        """
        super().__init__(
            agent_type=AgentType.MENTOR,
            name="Mentor Agent",
            description="Provides guidance and identifies knowledge gaps",
        )
        self.ai_service = ai_service
        self.memory_repo = memory_repo
    
    async def execute(self, context: Any) -> Dict[str, Any]:
        """Execute mentor's primary function: analyze logs and identify gaps.
        
        Args:
            context: Execution context (can be execution logs or task)
            
        Returns:
            Dictionary with analysis results and guidance
            
        Raises:
            DomainException: If execution fails
        """
        start_time = time.time()
        
        try:
            # Determine what type of execution is needed
            if isinstance(context, Task):
                result = await self.provide_task_mentorship(context)
            elif isinstance(context, dict) and "execution_logs" in context:
                result = await self.analyze_execution_logs(context["execution_logs"])
            else:
                # Default: analyze recent execution logs
                logs = await self._load_execution_logs()
                result = await self.analyze_execution_logs(logs)
            
            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)
            
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Mentor execution failed: {e}")
    
    async def provide_task_mentorship(self, task: Task) -> Dict[str, Any]:
        """Provide mentorship guidance for a specific task.
        
        Args:
            task: Task requiring mentorship
            
        Returns:
            Dictionary with mentorship guidance
        """
        mentorship = await self.ai_service.provide_mentorship(task)
        
        return {
            "task_id": task.task_id,
            "task_title": task.title,
            "mentorship": mentorship,
        }
    
    async def analyze_execution_logs(self, execution_logs: List[Dict]) -> Dict[str, Any]:
        """Analyze execution logs to identify patterns and gaps.
        
        Args:
            execution_logs: List of execution log entries
            
        Returns:
            Dictionary with identified gaps and recommendations
        """
        if not execution_logs:
            return {
                "gaps": [],
                "recommendations": ["No execution logs available for analysis"],
            }
        
        # Use AI service to analyze gaps
        gaps = await self.ai_service.analyze_gaps(execution_logs)
        
        # Generate recommendations based on gaps
        recommendations = self._generate_recommendations(gaps)
        
        return {
            "gaps": gaps,
            "recommendations": recommendations,
            "logs_analyzed": len(execution_logs),
        }
    
    def _generate_recommendations(self, gaps: List[Dict]) -> List[str]:
        """Generate recommendations based on identified gaps.
        
        Args:
            gaps: List of identified gaps
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Categorize gaps by severity
        high_severity = [g for g in gaps if g.get("severity") == "high"]
        medium_severity = [g for g in gaps if g.get("severity") == "medium"]
        
        if high_severity:
            recommendations.append(
                f"Address {len(high_severity)} high-severity gaps immediately"
            )
            for gap in high_severity:
                recommendations.append(f"- {gap.get('description')}")
        
        if medium_severity:
            recommendations.append(
                f"Plan to address {len(medium_severity)} medium-severity gaps"
            )
        
        # Categorize by type
        knowledge_gaps = [g for g in gaps if g.get("type") == "knowledge"]
        skill_gaps = [g for g in gaps if g.get("type") == "skill"]
        
        if knowledge_gaps:
            recommendations.append(
                f"Allocate time for learning to address {len(knowledge_gaps)} knowledge gaps"
            )
        
        if skill_gaps:
            recommendations.append(
                f"Practice and training needed for {len(skill_gaps)} skill gaps"
            )
        
        if not recommendations:
            recommendations.append("No critical gaps identified - maintain current trajectory")
        
        return recommendations
    
    async def _load_execution_logs(self) -> List[Dict]:
        """Load execution logs from memory.
        
        Returns:
            List of execution log entries
        """
        try:
            # Try to get execution logs from memory
            logs_memory = await self.memory_repo.get("logs")
            if logs_memory:
                return logs_memory.content.get("items", [])
            
            return []
        except Exception:
            return []
    
    async def identify_learning_needs(self, gaps: List[Dict]) -> List[Dict]:
        """Identify specific learning needs from gaps.
        
        Args:
            gaps: List of identified gaps
            
        Returns:
            List of learning needs with resources
        """
        learning_needs = []
        
        for gap in gaps:
            need = {
                "topic": gap.get("description"),
                "type": gap.get("type"),
                "priority": gap.get("severity"),
                "suggested_resources": self._suggest_resources(gap),
            }
            learning_needs.append(need)
        
        return learning_needs
    
    def _suggest_resources(self, gap: Dict) -> List[str]:
        """Suggest learning resources for a gap.
        
        Args:
            gap: Gap information
            
        Returns:
            List of suggested resources
        """
        resources = []
        gap_type = gap.get("type", "")
        
        if gap_type == "knowledge":
            resources.extend([
                "Official documentation",
                "Online courses (Coursera, Udemy)",
                "Technical books",
            ])
        elif gap_type == "skill":
            resources.extend([
                "Hands-on tutorials",
                "Practice projects",
                "Code katas",
            ])
        elif gap_type == "process":
            resources.extend([
                "Best practices guides",
                "Workflow templates",
                "Process documentation",
            ])
        
        return resources
