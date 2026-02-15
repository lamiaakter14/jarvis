"""Agent coordination service with priority-based task handling."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.repositories.i_task_repository import ITaskRepository
from jarvis_core.shared.constants import TaskStatus, TaskPriority, AgentType
from jarvis_core.shared.exceptions import DomainException


class AgentCoordinator:
    """Coordinates agent execution with priority-based task handling.
    
    Provides:
    - Priority-based task assignment
    - Multi-agent synchronization
    - Resource management
    - Performance optimization
    """
    
    def __init__(self, task_repository: ITaskRepository):
        """Initialize the agent coordinator.
        
        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository
        self._agent_registry: Dict[AgentType, Agent] = {}
    
    def register_agent(self, agent: Agent) -> None:
        """Register an agent for coordination.
        
        Args:
            agent: Agent instance to register
        """
        self._agent_registry[agent.agent_type] = agent
    
    def get_agent(self, agent_type: AgentType) -> Optional[Agent]:
        """Get a registered agent by type.
        
        Args:
            agent_type: Type of agent to retrieve
            
        Returns:
            Agent instance if found, None otherwise
        """
        return self._agent_registry.get(agent_type)
    
    async def coordinate_task_execution(
        self,
        context: Context,
        priority_threshold: Optional[TaskPriority] = None
    ) -> Dict[str, Any]:
        """Coordinate task execution across agents with priority handling.
        
        Args:
            context: Execution context
            priority_threshold: Minimum priority for tasks (default: all)
            
        Returns:
            Coordination results with execution statistics
        """
        # Get pending tasks sorted by priority
        filters = {"status": TaskStatus.PENDING}
        if priority_threshold:
            filters["priority"] = priority_threshold
        
        pending_tasks = await self.task_repository.list(filters=filters)
        
        if not pending_tasks:
            return {
                "status": "no_tasks",
                "message": "No pending tasks to execute",
                "executed": 0
            }
        
        # Sort tasks by priority (critical > high > medium > low)
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3
        }
        sorted_tasks = sorted(
            pending_tasks,
            key=lambda t: priority_order.get(t.priority, 999)
        )
        
        # Execute tasks based on agent availability
        results = {
            "total_tasks": len(sorted_tasks),
            "executed": 0,
            "failed": 0,
            "skipped": 0,
            "task_results": [],
            "start_time": datetime.now()
        }
        
        for task in sorted_tasks:
            # Get appropriate agent for task
            agent = self.get_agent(task.agent_type)
            
            if not agent:
                results["skipped"] += 1
                results["task_results"].append({
                    "task_id": task.task_id,
                    "status": "skipped",
                    "reason": f"No agent registered for {task.agent_type}"
                })
                continue
            
            # Execute task with agent
            try:
                task.mark_in_progress()
                await self.task_repository.save(task)
                
                result = await agent.execute(context)
                
                task.complete(result)
                await self.task_repository.save(task)
                
                results["executed"] += 1
                results["task_results"].append({
                    "task_id": task.task_id,
                    "status": "completed",
                    "agent_type": str(task.agent_type),
                    "priority": str(task.priority)
                })
                
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = {"error": str(e)}
                await self.task_repository.save(task)
                
                results["failed"] += 1
                results["task_results"].append({
                    "task_id": task.task_id,
                    "status": "failed",
                    "error": str(e),
                    "agent_type": str(task.agent_type)
                })
        
        results["end_time"] = datetime.now()
        results["duration_seconds"] = (
            results["end_time"] - results["start_time"]
        ).total_seconds()
        
        return results
    
    async def coordinate_agents_parallel(
        self,
        context: Context,
        agent_types: List[AgentType],
        max_concurrent: int = 3
    ) -> Dict[str, Any]:
        """Coordinate parallel agent execution with concurrency control.
        
        Args:
            context: Execution context
            agent_types: List of agent types to execute
            max_concurrent: Maximum concurrent agent executions
            
        Returns:
            Parallel execution results
        """
        agents = [self.get_agent(at) for at in agent_types if self.get_agent(at)]
        
        if not agents:
            raise DomainException("No agents available for execution")
        
        results = {
            "total_agents": len(agents),
            "successful": 0,
            "failed": 0,
            "agent_results": []
        }
        
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(agent: Agent):
            async with semaphore:
                try:
                    result = await agent.execute(context)
                    return {
                        "agent_id": agent.agent_id,
                        "agent_type": str(agent.agent_type),
                        "status": "success",
                        "result": result
                    }
                except Exception as e:
                    return {
                        "agent_id": agent.agent_id,
                        "agent_type": str(agent.agent_type),
                        "status": "failed",
                        "error": str(e)
                    }
        
        # Execute agents in parallel with concurrency limit
        agent_futures = [execute_with_semaphore(agent) for agent in agents]
        agent_results = await asyncio.gather(*agent_futures, return_exceptions=False)
        
        # Aggregate results
        for result in agent_results:
            results["agent_results"].append(result)
            if result["status"] == "success":
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    async def synchronize_strategic_agents(
        self,
        context: Context
    ) -> Dict[str, Any]:
        """Synchronize STRATEGIST, EXECUTOR, and MENTOR agents.
        
        Executes agents in a coordinated workflow:
        1. STRATEGIST: Plans and prioritizes tasks
        2. EXECUTOR: Executes high-priority tasks
        3. MENTOR: Provides guidance and feedback
        
        Args:
            context: Execution context
            
        Returns:
            Synchronized execution results
        """
        workflow_results = {
            "workflow": "strategic_agents_sync",
            "steps": [],
            "overall_status": "success"
        }
        
        # Step 1: STRATEGIST - Planning
        strategist = self.get_agent(AgentType.STRATEGIST)
        if strategist:
            try:
                strategy_result = await strategist.execute(context)
                workflow_results["steps"].append({
                    "step": "strategy",
                    "agent": "STRATEGIST",
                    "status": "success",
                    "result": strategy_result
                })
            except Exception as e:
                workflow_results["steps"].append({
                    "step": "strategy",
                    "agent": "STRATEGIST",
                    "status": "failed",
                    "error": str(e)
                })
                workflow_results["overall_status"] = "partial_failure"
        
        # Step 2: EXECUTOR - Task execution
        executor = self.get_agent(AgentType.EXECUTOR)
        if executor:
            try:
                execution_result = await executor.execute(context)
                workflow_results["steps"].append({
                    "step": "execution",
                    "agent": "EXECUTOR",
                    "status": "success",
                    "result": execution_result
                })
            except Exception as e:
                workflow_results["steps"].append({
                    "step": "execution",
                    "agent": "EXECUTOR",
                    "status": "failed",
                    "error": str(e)
                })
                workflow_results["overall_status"] = "partial_failure"
        
        # Step 3: MENTOR - Guidance and feedback
        mentor = self.get_agent(AgentType.MENTOR)
        if mentor:
            try:
                mentor_result = await mentor.execute(context)
                workflow_results["steps"].append({
                    "step": "mentoring",
                    "agent": "MENTOR",
                    "status": "success",
                    "result": mentor_result
                })
            except Exception as e:
                workflow_results["steps"].append({
                    "step": "mentoring",
                    "agent": "MENTOR",
                    "status": "failed",
                    "error": str(e)
                })
                workflow_results["overall_status"] = "partial_failure"
        
        return workflow_results
