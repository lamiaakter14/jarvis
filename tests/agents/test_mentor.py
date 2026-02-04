"""
Unit tests for the Mentor agent.
"""
import unittest
import tempfile
import shutil
from core.memory_manager import MemoryManager
from agents.mentor import Mentor


class TestMentor(unittest.TestCase):
    """Test cases for the Mentor agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.mentor = Mentor(self.memory_manager)
        
        # Create test data
        self._create_test_data()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data(self):
        """Create test data for mentor."""
        gaps_data = {
            "unresolved_gaps": [
                {
                    "id": "gap_1",
                    "description": "Understanding loops",
                    "evidence": ["Failed test"],
                    "suggested_remediation": ["Practice"]
                }
            ],
            "body": "# Knowledge Gaps"
        }
        self.memory_manager.save_knowledge("gaps.md", gaps_data)
        
        reflections_data = {
            "reflections": [
                {
                    "date": "2026-02-01",
                    "learning_summary": {
                        "facts_learned": ["Python basics", "Variables"]
                    },
                    "error_analysis": [],
                    "evolution_recommendations": ["Keep practicing"]
                }
            ],
            "body": "# Reflections"
        }
        self.memory_manager.save_knowledge("reflections.md", reflections_data)

    def test_provide_feedback_success(self):
        """Test feedback for successful task."""
        task = {
            "task": "Complete Python exercise",
            "status": "success",
            "errors": []
        }
        
        feedback = self.mentor.provide_feedback(task)
        
        self.assertIsInstance(feedback, dict)
        self.assertIn("task", feedback)
        self.assertIn("feedback", feedback)
        self.assertEqual(feedback["task"], task["task"])
        self.assertIn("Great work", feedback["feedback"][0])

    def test_provide_feedback_with_errors(self):
        """Test feedback for task with errors."""
        task = {
            "task": "Debug Python code",
            "status": "failed",
            "errors": [
                {"message": "Syntax error"},
                {"message": "Type error"}
            ]
        }
        
        feedback = self.mentor.provide_feedback(task)
        
        self.assertIsInstance(feedback, dict)
        self.assertIn("feedback", feedback)
        self.assertGreater(len(feedback["feedback"]), 0)

    def test_assess_knowledge_depth(self):
        """Test knowledge depth assessment."""
        topic = "Python basics"
        
        assessment = self.mentor.assess_knowledge_depth(topic)
        
        self.assertIsInstance(assessment, dict)
        self.assertIn("topic", assessment)
        self.assertIn("depth_score", assessment)
        self.assertIn("status", assessment)
        self.assertEqual(assessment["topic"], topic)
        self.assertGreaterEqual(assessment["depth_score"], 0)
        self.assertLessEqual(assessment["depth_score"], 100)

    def test_socratic_questioning(self):
        """Test Socratic question generation."""
        topic = "Recursion"
        
        question = self.mentor.socratic_questioning(topic)
        
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)
        self.assertIn(topic, question)

    def test_mentor_task(self):
        """Test complete mentorship process for a task."""
        task = {
            "task": "Learn about functions",
            "status": "in_progress",
            "errors": []
        }
        
        mentorship = self.mentor.mentor_task(task)
        
        self.assertIsInstance(mentorship, dict)
        self.assertIn("task", mentorship)
        self.assertIn("feedback", mentorship)
        self.assertIn("socratic_question", mentorship)
        self.assertIn("recommendations", mentorship)

    def test_provide_learning_suggestions(self):
        """Test learning suggestions generation."""
        task = {
            "task": "Study data structures",
            "priority": "high"
        }
        
        suggestions = self.mentor.provide_learning_suggestions(task)
        
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)

    def test_edge_case_missing_data(self):
        """Test behavior with missing reflections data."""
        # Clear reflections
        shutil.rmtree(self.test_dir)
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)
        self.mentor = Mentor(self.memory_manager)
        
        # Should handle missing data gracefully
        assessment = self.mentor.assess_knowledge_depth("Python")
        self.assertEqual(assessment["depth_score"], 0)


if __name__ == "__main__":
    unittest.main()
