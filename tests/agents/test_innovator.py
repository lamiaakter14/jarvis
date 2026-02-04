"""
Unit tests for the Innovator agent.
"""
import unittest
import tempfile
import shutil
from core.memory_manager import MemoryManager
from agents.innovator import Innovator


class TestInnovator(unittest.TestCase):
    """Test cases for the Innovator agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.innovator = Innovator(self.memory_manager)
        
        # Create test data
        self._create_test_data()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data(self):
        """Create test data for innovator."""
        feedback_data = {
            "task1": {
                "status": "failed",
                "errors": ["Syntax error", "Logic error"]
            },
            "task2": {
                "status": "success",
                "errors": []
            }
        }
        self.memory_manager.save_working_memory("execution_logs/feedback.json", feedback_data)
        
        gaps_data = {
            "unresolved_gaps": [
                {
                    "id": "gap_1",
                    "description": "Understanding async/await",
                    "suggested_remediation": ["Study async patterns"]
                }
            ],
            "body": "# Knowledge Gaps"
        }
        self.memory_manager.save_knowledge("gaps.md", gaps_data)
        
        reflections_data = {
            "reflections": [
                {
                    "date": "2026-02-01",
                    "evolution_recommendations": ["Focus on fundamentals"]
                },
                {
                    "date": "2026-02-02",
                    "evolution_recommendations": ["Practice more"]
                }
            ],
            "body": "# Reflections"
        }
        self.memory_manager.save_knowledge("reflections.md", reflections_data)

    def test_analyze_feedback_and_gaps(self):
        """Test analysis of feedback and knowledge gaps."""
        insights = self.innovator.analyze_feedback_and_gaps()
        
        self.assertIsInstance(insights, dict)
        self.assertIn("learning_optimizations", insights)
        self.assertIn("task_improvements", insights)
        self.assertIn("patterns_detected", insights)

    def test_generate_creative_suggestions(self):
        """Test generation of creative suggestions."""
        insights = {
            "learning_optimizations": ["Study topic A"],
            "task_improvements": ["Improve task B"],
            "patterns_detected": ["Pattern C detected"]
        }
        
        suggestions = self.innovator.generate_creative_suggestions(insights)
        
        self.assertIsInstance(suggestions, dict)
        self.assertIn("creative_suggestions", suggestions)
        self.assertIsInstance(suggestions["creative_suggestions"], list)
        self.assertGreater(len(suggestions["creative_suggestions"]), 0)

    def test_create_innovations(self):
        """Test complete innovation creation process."""
        # Should not raise exceptions
        try:
            self.innovator.create_innovations()
        except Exception as e:
            self.fail(f"create_innovations raised exception: {e}")
        
        # Verify innovations were saved
        innovations = self.memory_manager.get_working_memory("innovator/innovations.json")
        self.assertIsInstance(innovations, dict)
        self.assertIn("creative_suggestions", innovations)

    def test_edge_case_no_failures(self):
        """Test behavior when there are no task failures."""
        # Create data with only successful tasks
        feedback_data = {
            "task1": {"status": "success", "errors": []},
            "task2": {"status": "success", "errors": []}
        }
        self.memory_manager.save_working_memory("execution_logs/feedback.json", feedback_data)
        
        insights = self.innovator.analyze_feedback_and_gaps()
        
        # Should still generate insights
        self.assertIsInstance(insights, dict)
        self.assertIn("learning_optimizations", insights)

    def test_edge_case_empty_data(self):
        """Test behavior with empty or missing data."""
        # Clear test data
        shutil.rmtree(self.test_dir)
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.innovator = Innovator(self.memory_manager)
        
        # Should handle missing data gracefully
        insights = self.innovator.analyze_feedback_and_gaps()
        self.assertIsInstance(insights, dict)


if __name__ == "__main__":
    unittest.main()
