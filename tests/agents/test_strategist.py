"""
Unit tests for the Strategist agent.
"""
import unittest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import date
from core.memory_manager import MemoryManager
from agents.strategist import Strategist


class TestStrategist(unittest.TestCase):
    """Test cases for the Strategist agent."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test memory
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.strategist = Strategist(self.memory_manager)
        
        # Create test data
        self._create_test_data()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data(self):
        """Create test data for strategist."""
        # Create test roadmap
        roadmap_data = {
            "milestones": [
                {
                    "title": "Complete Python basics",
                    "due_date": "2026-03-01",
                    "status": "in_progress"
                },
                {
                    "title": "Build first AI project",
                    "due_date": "2026-04-01",
                    "status": "pending"
                }
            ],
            "body": "# Learning Roadmap\nPlan for skill development."
        }
        self.memory_manager.save_knowledge("roadmap.md", roadmap_data)
        
        # Create test gaps
        gaps_data = {
            "unresolved_gaps": [
                {
                    "id": "gap_1",
                    "description": "Understanding recursion",
                    "evidence": ["Failed quiz on recursion", "Incorrect recursive function"],
                    "suggested_remediation": ["Practice recursive problems"]
                }
            ],
            "body": "# Knowledge Gaps"
        }
        self.memory_manager.save_knowledge("gaps.md", gaps_data)
        
        # Create test context
        context_data = {
            "date": str(date.today()),
            "current_focus": ["Python", "Algorithms"],
            "energy_level": "high"
        }
        self.memory_manager.save_working_memory("daily_context.json", context_data)

    def test_generate_plan(self):
        """Test that generate_plan creates a valid daily plan."""
        plan = self.strategist.generate_plan()
        
        # Verify plan structure
        self.assertIsInstance(plan, dict)
        self.assertIn("date", plan)
        self.assertIn("tasks", plan)
        self.assertIsInstance(plan["tasks"], list)
        
        # Verify tasks have required fields
        if plan["tasks"]:
            task = plan["tasks"][0]
            self.assertIn("task", task)
            self.assertIn("priority", task)
            self.assertIn("cognitive_load", task)

    def test_prioritize_tasks(self):
        """Test task prioritization logic."""
        roadmap = self.memory_manager.get_knowledge("roadmap.md")
        gaps = self.memory_manager.get_knowledge("gaps.md")
        context = self.memory_manager.get_working_memory("daily_context.json")
        
        tasks = self.strategist.prioritize_tasks(roadmap, gaps, context)
        
        # Verify tasks are sorted by ROI
        self.assertIsInstance(tasks, list)
        if len(tasks) > 1:
            for i in range(len(tasks) - 1):
                self.assertGreaterEqual(tasks[i]["roi"], tasks[i + 1]["roi"])

    def test_calculate_learning_roi(self):
        """Test learning ROI calculation."""
        gap = {
            "description": "Understanding recursion",
            "evidence": ["Failed quiz", "Incorrect function", "Confused in lecture"]
        }
        
        roi = self.strategist.calculate_learning_roi(gap)
        
        # ROI should be positive and based on evidence count
        self.assertGreater(roi, 0)
        self.assertEqual(roi, len(gap["evidence"]) * 1.5)

    def test_create_schedule(self):
        """Test schedule creation with time blocking."""
        tasks = [
            {"task": "Task 1", "cognitive_load": "high", "roi": 5.0, "priority": "high"},
            {"task": "Task 2", "cognitive_load": "medium", "roi": 3.0, "priority": "medium"},
            {"task": "Task 3", "cognitive_load": "low", "roi": 1.0, "priority": "low"},
        ]
        context = {"date": str(date.today())}
        
        schedule = self.strategist.create_schedule(tasks, context)
        
        # Verify schedule respects time constraints
        self.assertIsInstance(schedule, list)
        total_time = sum([
            int(task["time_allocated"].split()[0]) 
            for task in schedule
        ])
        self.assertLessEqual(total_time, 8)

    def test_edge_case_empty_data(self):
        """Test behavior with empty or missing data."""
        # Clear test data
        shutil.rmtree(self.test_dir)
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.strategist = Strategist(self.memory_manager)
        
        # Should handle missing data gracefully
        plan = self.strategist.generate_plan()
        self.assertIsInstance(plan, dict)
        self.assertIn("tasks", plan)


if __name__ == "__main__":
    unittest.main()
