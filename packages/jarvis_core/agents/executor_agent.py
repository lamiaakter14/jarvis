"""Executor Agent - Phase 4: Task execution engine."""

from typing import Dict, List, Optional
from datetime import datetime, timezone


class ExecutorAgent:
    """Executes approved tasks with status tracking."""
    
    def __init__(self):
        self.name = "ExecutorAgent"
        self.version = "4.0.0"
        self.task_queue: List[Dict] = []
        self.completed_tasks: List[Dict] = []
    
    def queue_tasks(self, project: Dict) -> List[Dict]:
        """Queue all tasks from a project for execution."""
        tasks = []
        for task in project.get("tasks", []):
            task_copy = {
                **task,
                "project_id": project["id"],
                "project_title": project["title"],
                "queued_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "execution_status": "queued",  # queued → running → done → failed
                "started_at": None,
                "completed_at": None,
            }
            self.task_queue.append(task_copy)
            tasks.append(task_copy)
        
        return tasks
    
    def execute_next(self) -> Optional[Dict]:
        """Execute the next queued task."""
        for task in self.task_queue:
            if task["execution_status"] == "queued":
                task["execution_status"] = "running"
                task["started_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                return task
        return None
    
    def complete_task(self, task_id: str) -> Optional[Dict]:
        """Mark a task as completed."""
        for task in self.task_queue:
            if task["id"] == task_id:
                task["execution_status"] = "done"
                task["completed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                self.completed_tasks.append(task)
                self.task_queue.remove(task)
                return task
        return None
    
    def fail_task(self, task_id: str, reason: str = "") -> Optional[Dict]:
        """Mark a task as failed."""
        for task in self.task_queue:
            if task["id"] == task_id:
                task["execution_status"] = "failed"
                task["fail_reason"] = reason
                return task
        return None
    
    def get_queue_status(self) -> Dict:
        """Get current execution queue status."""
        return {
            "total_queued": len(self.task_queue),
            "running": len([t for t in self.task_queue if t["execution_status"] == "running"]),
            "pending": len([t for t in self.task_queue if t["execution_status"] == "queued"]),
            "completed": len(self.completed_tasks),
            "failed": len([t for t in self.task_queue if t["execution_status"] == "failed"]),
            "tasks": self.task_queue[:5],  # Latest 5
        }
    
    def run_all(self) -> List[Dict]:
        """Execute all queued tasks (simulation)."""
        results = []
        for task in self.task_queue:
            if task["execution_status"] == "queued":
                task["execution_status"] = "done"
                task["started_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                task["completed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                self.completed_tasks.append(task)
                results.append(task)
        
        self.task_queue = [t for t in self.task_queue if t["execution_status"] != "done"]
        return results