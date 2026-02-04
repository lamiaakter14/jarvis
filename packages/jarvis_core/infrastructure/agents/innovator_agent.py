"""Innovator agent implementation."""

from typing import Any, Dict, List
import time

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException


class InnovatorAgent(Agent):
    """Innovator agent for creative solutions and improvements.
    
    The innovator analyzes patterns, performance data, and context to
    generate novel ideas, process improvements, and creative solutions.
    """
    
    def __init__(
        self,
        ai_service: IAIService,
        memory_repo: IMemoryRepository,
    ):
        """Initialize innovator agent.
        
        Args:
            ai_service: AI service for innovation generation
            memory_repo: Memory repository for storing innovations
        """
        super().__init__(
            agent_type=AgentType.INNOVATOR,
            name="Innovator Agent",
            description="Generates creative solutions and innovative approaches",
        )
        self.ai_service = ai_service
        self.memory_repo = memory_repo
    
    async def execute(self, context: Context) -> List[Innovation]:
        """Execute innovator's primary function: generate innovations.
        
        Args:
            context: Current execution context
            
        Returns:
            List of generated innovations
            
        Raises:
            DomainException: If execution fails
        """
        start_time = time.time()
        
        try:
            # Generate innovations using AI service
            innovations = await self.ai_service.generate_innovations(context)
            
            # Store innovations in memory
            await self._store_innovations(innovations)
            
            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)
            
            return innovations
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Innovator execution failed: {e}")
    
    async def _store_innovations(self, innovations: List[Innovation]) -> None:
        """Store innovations in memory.
        
        Args:
            innovations: List of innovations to store
        """
        try:
            # Try to get existing innovations
            innovations_memory = await self.memory_repo.get("innovations")
            
            # Convert innovations to dictionaries
            innovations_data = [self._innovation_to_dict(inn) for inn in innovations]
            
            if innovations_memory:
                # Append to existing innovations
                existing = innovations_memory.content.get("items", [])
                existing.extend(innovations_data)
                innovations_memory.update_content({"items": existing})
                await self.memory_repo.save(innovations_memory)
            else:
                # Create new innovations memory
                innovations_memory = Memory(
                    type=MemoryType.WORKING,
                    key="innovations",
                    content={"items": innovations_data},
                )
                await self.memory_repo.save(innovations_memory)
        
        except Exception as e:
            # Log error but don't fail the execution
            print(f"Warning: Failed to store innovations: {e}")
    
    def _innovation_to_dict(self, innovation: Innovation) -> Dict[str, Any]:
        """Convert Innovation entity to dictionary.
        
        Args:
            innovation: Innovation entity
            
        Returns:
            Dictionary representation
        """
        return {
            "innovation_id": innovation.innovation_id,
            "title": innovation.title,
            "description": innovation.description,
            "category": innovation.category,
            "impact_score": innovation.impact_score,
            "status": innovation.status,
            "created_at": innovation.created_at.isoformat(),
            "created_by": innovation.created_by,
        }
    
    async def get_high_impact_innovations(self) -> List[Dict[str, Any]]:
        """Get all high-impact innovations.
        
        Returns:
            List of high-impact innovations
        """
        try:
            innovations_memory = await self.memory_repo.get("innovations")
            if not innovations_memory:
                return []
            
            all_innovations = innovations_memory.content.get("items", [])
            return [
                inn for inn in all_innovations
                if inn.get("impact_score", 0) >= 0.7
            ]
        except Exception:
            return []
    
    async def get_innovations_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get innovations filtered by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of innovations in the category
        """
        try:
            innovations_memory = await self.memory_repo.get("innovations")
            if not innovations_memory:
                return []
            
            all_innovations = innovations_memory.content.get("items", [])
            return [
                inn for inn in all_innovations
                if inn.get("category") == category
            ]
        except Exception:
            return []
    
    async def analyze_innovation_trends(self) -> Dict[str, Any]:
        """Analyze trends in generated innovations.
        
        Returns:
            Dictionary with trend analysis
        """
        try:
            innovations_memory = await self.memory_repo.get("innovations")
            if not innovations_memory:
                return {
                    "total_innovations": 0,
                    "categories": {},
                    "average_impact": 0.0,
                }
            
            all_innovations = innovations_memory.content.get("items", [])
            
            # Calculate statistics
            total = len(all_innovations)
            categories = {}
            total_impact = 0.0
            
            for inn in all_innovations:
                category = inn.get("category", "general")
                categories[category] = categories.get(category, 0) + 1
                total_impact += inn.get("impact_score", 0)
            
            return {
                "total_innovations": total,
                "categories": categories,
                "average_impact": total_impact / total if total > 0 else 0.0,
                "high_impact_count": len([
                    inn for inn in all_innovations
                    if inn.get("impact_score", 0) >= 0.7
                ]),
            }
        except Exception as e:
            return {
                "error": str(e),
                "total_innovations": 0,
            }
    
    async def suggest_quick_wins(self) -> List[Dict[str, Any]]:
        """Suggest quick wins - high impact, easy to implement innovations.
        
        Returns:
            List of quick win innovations
        """
        try:
            innovations_memory = await self.memory_repo.get("innovations")
            if not innovations_memory:
                return []
            
            all_innovations = innovations_memory.content.get("items", [])
            
            # Filter for high impact innovations that are proposed (not yet implemented)
            quick_wins = [
                inn for inn in all_innovations
                if inn.get("impact_score", 0) >= 0.7
                and inn.get("status") == "proposed"
            ]
            
            # Sort by impact score
            quick_wins.sort(key=lambda x: x.get("impact_score", 0), reverse=True)
            
            return quick_wins[:5]  # Return top 5
        except Exception:
            return []
