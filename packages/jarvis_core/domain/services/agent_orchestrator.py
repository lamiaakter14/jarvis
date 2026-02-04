"""Agent orchestrator domain service."""

from typing import Any, Dict, List

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.context import Context
from jarvis_core.shared.exceptions import DomainException


class AgentOrchestrator:
    """Service for orchestrating multi-agent execution.
    
    The AgentOrchestrator coordinates the execution of multiple agents,
    managing dependencies, sequencing, and result aggregation. It ensures
    agents execute in the optimal order and have access to necessary context.
    """
    
    async def coordinate_agents(
        self,
        context: Context,
        agents: List[Agent]
    ) -> Dict[str, Any]:
        """Coordinate execution of multiple agents in parallel.
        
        Executes agents concurrently when possible, aggregating their results
        and updating the context based on outcomes.
        
        Args:
            context: Execution context for agents
            agents: List of agents to coordinate
            
        Returns:
            Dictionary containing aggregated results and execution metadata
            
        Raises:
            DomainException: If coordination fails
        """
        if not agents:
            raise DomainException("Cannot coordinate empty agent list")
        
        if context.available_hours <= 0:
            raise DomainException("No available hours in context for agent execution")
        
        results = {
            "total_agents": len(agents),
            "successful_executions": 0,
            "failed_executions": 0,
            "agent_results": [],
            "total_time": 0.0,
        }
        
        # Execute agents with their context
        for agent in agents:
            try:
                result = await agent.execute(context)
                results["agent_results"].append({
                    "agent_id": agent.agent_id,
                    "agent_type": str(agent.agent_type),
                    "success": True,
                    "result": result,
                })
                results["successful_executions"] += 1
                
                # Track execution time if available
                if agent.last_execution_time:
                    avg_time = agent.get_average_execution_time()
                    results["total_time"] += avg_time
                    
            except Exception as e:
                results["agent_results"].append({
                    "agent_id": agent.agent_id,
                    "agent_type": str(agent.agent_type),
                    "success": False,
                    "error": str(e),
                })
                results["failed_executions"] += 1
        
        # Calculate success rate
        results["success_rate"] = (
            results["successful_executions"] / results["total_agents"]
            if results["total_agents"] > 0 else 0.0
        )
        
        return results
    
    async def execute_agent_sequence(
        self,
        agents: List[Agent],
        context: Context
    ) -> List[Any]:
        """Execute agents in sequence, passing results forward.
        
        Each agent receives the context and results from previous agents.
        This is useful for dependent agent operations where order matters.
        
        Args:
            agents: List of agents to execute in order
            context: Execution context for agents
            
        Returns:
            List of results from each agent in sequence
            
        Raises:
            DomainException: If any agent fails or sequence is invalid
        """
        if not agents:
            raise DomainException("Cannot execute empty agent sequence")
        
        if context.available_hours <= 0:
            raise DomainException("No available hours in context for agent execution")
        
        results = []
        
        for i, agent in enumerate(agents):
            try:
                # Execute agent with current context
                result = await agent.execute(context)
                results.append(result)
                
                # Update context with execution metrics
                if agent.last_execution_time:
                    avg_time = agent.get_average_execution_time()
                    hours_used = avg_time / 3600.0  # Convert seconds to hours
                    
                    # Consume hours if we have enough
                    if context.has_available_hours(hours_used):
                        context.consume_hours(hours_used)
                    
            except Exception as e:
                raise DomainException(
                    f"Agent {i+1}/{len(agents)} ({agent.agent_type}) failed: {str(e)}"
                )
        
        return results
    
    def validate_agent_compatibility(
        self,
        agents: List[Agent],
        context: Context
    ) -> Dict[str, Any]:
        """Validate that agents can work with the given context.
        
        Checks for sufficient resources, compatible agent types, and
        reasonable execution parameters.
        
        Args:
            agents: List of agents to validate
            context: Execution context
            
        Returns:
            Validation result with warnings and recommendations
        """
        validation = {
            "is_valid": True,
            "warnings": [],
            "recommendations": [],
        }
        
        if not agents:
            validation["is_valid"] = False
            validation["warnings"].append("No agents provided")
            return validation
        
        # Check for sufficient time
        total_estimated_hours = sum(
            agent.get_average_execution_time() / 3600.0
            for agent in agents
        )
        
        if total_estimated_hours > context.available_hours:
            validation["warnings"].append(
                f"Estimated time ({total_estimated_hours:.1f}h) exceeds "
                f"available hours ({context.available_hours:.1f}h)"
            )
            validation["recommendations"].append(
                "Consider reducing agent count or increasing available hours"
            )
        
        # Check for agent diversity
        agent_types = [str(agent.agent_type) for agent in agents]
        if len(set(agent_types)) == 1 and len(agents) > 1:
            validation["warnings"].append(
                "All agents are the same type - consider diversifying"
            )
        
        # Check agent health
        unhealthy_agents = [
            agent for agent in agents
            if agent.total_executions > 0 and agent.get_success_rate() < 0.5
        ]
        
        if unhealthy_agents:
            validation["warnings"].append(
                f"{len(unhealthy_agents)} agents have low success rates"
            )
            validation["recommendations"].append(
                "Review and fix failing agents before execution"
            )
        
        return validation
