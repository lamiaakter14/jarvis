"""
Unit tests for the Amplifier agent.
"""
import unittest
import tempfile
import shutil
from core.memory_manager import MemoryManager
from agents.amplifier import Amplifier


class TestAmplifier(unittest.TestCase):
    """Test cases for the Amplifier agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.amplifier = Amplifier(self.memory_manager)
        
        # Create test data
        self._create_test_data()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data(self):
        """Create test data for amplifier."""
        feedback_data = {
            "task1": {"status": "success", "errors": []},
            "task2": {"status": "failed", "errors": ["Error A"]},
            "task3": {"status": "success", "errors": []},
            "task4": {"status": "manual_pending", "errors": []}
        }
        self.memory_manager.save_working_memory("execution_logs/feedback.json", feedback_data)
        
        reflections_data = {
            "reflections": [
                {
                    "date": "2026-02-01",
                    "evolution_recommendations": ["Improve focus", "Practice daily"]
                }
            ],
            "body": "# Reflections"
        }
        self.memory_manager.save_knowledge("reflections.md", reflections_data)
        
        gaps_data = {
            "unresolved_gaps": [
                {"id": "gap_1", "description": "Gap 1"},
                {"id": "gap_2", "description": "Gap 2"}
            ],
            "body": "# Knowledge Gaps"
        }
        self.memory_manager.save_knowledge("gaps.md", gaps_data)

    def test_analyze_performance(self):
        """Test performance analysis."""
        results = self.amplifier.analyze_performance()
        
        self.assertIsInstance(results, dict)
        self.assertIn("performance_metrics", results)
        self.assertIn("insights", results)
        
        metrics = results["performance_metrics"]
        self.assertIn("tasks_completed", metrics)
        self.assertIn("tasks_failed", metrics)
        self.assertIn("total_tasks", metrics)
        self.assertEqual(metrics["tasks_completed"], 2)
        self.assertEqual(metrics["tasks_failed"], 1)
        self.assertEqual(metrics["total_tasks"], 4)

    def test_propose_optimizations(self):
        """Test optimization proposals."""
        performance_summary = {
            "performance_metrics": {
                "tasks_completed": 2,
                "tasks_failed": 2,
                "total_tasks": 4,
                "recommendation_count": 3
            },
            "insights": []
        }
        
        optimizations = self.amplifier.propose_optimizations(performance_summary)
        
        self.assertIsInstance(optimizations, dict)
        self.assertIn("proposed_optimizations", optimizations)
        self.assertIsInstance(optimizations["proposed_optimizations"], list)
        self.assertGreater(len(optimizations["proposed_optimizations"]), 0)

    def test_amplify(self):
        """Test complete amplification process."""
        results = self.amplifier.amplify()
        
        self.assertIsInstance(results, dict)
        self.assertIn("performance_summary", results)
        self.assertIn("optimizations", results)
        
        # Verify results were saved
        saved_results = self.memory_manager.get_working_memory("amplifier/performance_summary.json")
        self.assertEqual(saved_results, results)

    def test_high_failure_rate_optimization(self):
        """Test optimization for high failure rate."""
        performance_summary = {
            "performance_metrics": {
                "tasks_completed": 1,
                "tasks_failed": 3,
                "total_tasks": 4,
                "recommendation_count": 2
            },
            "insights": []
        }
        
        optimizations = self.amplifier.propose_optimizations(performance_summary)
        
        # Should suggest reducing task difficulty
        suggestions = optimizations["proposed_optimizations"]
        has_difficulty_suggestion = any(
            "difficulty" in s.lower() or "preparation" in s.lower()
            for s in suggestions
        )
        self.assertTrue(has_difficulty_suggestion)

    def test_edge_case_no_tasks(self):
        """Test behavior with no tasks executed."""
        # Create empty feedback
        empty_feedback = {}
        self.memory_manager.save_working_memory("execution_logs/feedback.json", empty_feedback)
        
        results = self.amplifier.analyze_performance()
        
        self.assertIsInstance(results, dict)
        metrics = results["performance_metrics"]
        self.assertEqual(metrics["total_tasks"], 0)

    def test_edge_case_all_success(self):
        """Test behavior when all tasks succeed."""
        success_feedback = {
            "task1": {"status": "success", "errors": []},
            "task2": {"status": "success", "errors": []}
        }
        self.memory_manager.save_working_memory("execution_logs/feedback.json", success_feedback)
        
        results = self.amplifier.analyze_performance()
        
        metrics = results["performance_metrics"]
        self.assertEqual(metrics["tasks_completed"], 2)
        self.assertEqual(metrics["tasks_failed"], 0)


if __name__ == "__main__":
    unittest.main()
