"""
Unit tests for the Executor agent.
"""
import unittest
import tempfile
import shutil
import os
from core.memory_manager import MemoryManager
from agents.executor import Executor


class TestExecutor(unittest.TestCase):
    """Test cases for the Executor agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.executor = Executor(self.memory_manager)
        
        # Create test data
        self._create_test_data()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data(self):
        """Create test data for executor."""
        daily_plan = {
            "date": "2026-02-04",
            "tasks": [
                {
                    "task": "Test manual task",
                    "type": "manual",
                    "details": {"instructions": "Complete manually"}
                }
            ]
        }
        self.memory_manager.save_working_memory("daily_plan.json", daily_plan)

    def test_execute_manual_task(self):
        """Test execution of manual task."""
        task = {
            "task": "Review documentation",
            "type": "manual",
            "details": {"instructions": "Read docs"}
        }
        
        log = self.executor.execute_task(task)
        
        self.assertIsInstance(log, dict)
        self.assertIn("task", log)
        self.assertIn("status", log)
        self.assertEqual(log["status"], "manual_pending")
        self.assertEqual(log["task"], task["task"])

    def test_execute_unrecognized_task(self):
        """Test execution of unrecognized task type."""
        task = {
            "task": "Unknown task",
            "type": "unknown_type",
            "details": {}
        }
        
        log = self.executor.execute_task(task)
        
        self.assertEqual(log["status"], "failed")
        self.assertGreater(len(log["errors"]), 0)
        self.assertIn("Unrecognized task type", log["errors"][0])

    def test_execute_script_file_not_found(self):
        """Test execution when script file doesn't exist."""
        task = {
            "task": "Run script",
            "type": "script",
            "details": {"script_path": "/nonexistent/script.py"}
        }
        
        log = self.executor.execute_task(task)
        
        self.assertEqual(log["status"], "failed")
        self.assertGreater(len(log["errors"]), 0)

    def test_save_execution_logs(self):
        """Test saving execution logs."""
        logs = {
            "task1": {"status": "success", "output": "Done"},
            "task2": {"status": "failed", "errors": ["Error"]}
        }
        
        self.executor.save_execution_logs(logs)
        
        # Verify logs were saved
        saved_logs = self.memory_manager.get_working_memory("execution_logs/logs.json")
        self.assertEqual(saved_logs, logs)

    def test_run_tasks(self):
        """Test running all tasks from daily plan."""
        # This test verifies the integration of task execution
        # Should not raise exceptions
        try:
            self.executor.run_tasks()
        except Exception as e:
            self.fail(f"run_tasks raised exception: {e}")

    def test_edge_case_empty_daily_plan(self):
        """Test behavior with empty daily plan."""
        # Create empty plan
        empty_plan = {"date": "2026-02-04", "tasks": []}
        self.memory_manager.save_working_memory("daily_plan.json", empty_plan)
        
        # Should handle empty plan gracefully
        try:
            self.executor.run_tasks()
        except Exception as e:
            self.fail(f"run_tasks with empty plan raised exception: {e}")


if __name__ == "__main__":
    unittest.main()
