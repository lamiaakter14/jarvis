"""
Unit tests for the Memory Manager.
"""
import unittest
import tempfile
import shutil
import json
from pathlib import Path
from core.memory_manager import MemoryManager


class TestMemoryManager(unittest.TestCase):
    """Test cases for the Memory Manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(memory_dir=self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test memory manager initialization."""
        # Verify directories were created
        working_path = Path(self.test_dir) / "working"
        knowledge_path = Path(self.test_dir) / "knowledge"
        execution_logs_path = working_path / "execution_logs"
        
        self.assertTrue(working_path.exists())
        self.assertTrue(knowledge_path.exists())
        self.assertTrue(execution_logs_path.exists())

    def test_save_and_get_working_memory(self):
        """Test saving and retrieving working memory."""
        test_data = {
            "date": "2026-02-04",
            "tasks": ["Task 1", "Task 2"],
            "status": "active"
        }
        
        # Save data
        self.memory_manager.save_working_memory("test_data.json", test_data)
        
        # Retrieve data
        retrieved_data = self.memory_manager.get_working_memory("test_data.json")
        
        self.assertEqual(retrieved_data, test_data)

    def test_get_nonexistent_working_memory(self):
        """Test retrieving nonexistent working memory file."""
        data = self.memory_manager.get_working_memory("nonexistent.json")
        
        # Should return empty dict
        self.assertEqual(data, {})

    def test_save_and_get_knowledge(self):
        """Test saving and retrieving knowledge memory."""
        test_data = {
            "milestones": ["Milestone 1", "Milestone 2"],
            "body": "# Test Knowledge\nThis is test content."
        }
        
        # Save data
        self.memory_manager.save_knowledge("test_knowledge.md", test_data)
        
        # Verify file was created
        knowledge_path = Path(self.test_dir) / "knowledge" / "test_knowledge.md"
        self.assertTrue(knowledge_path.exists())

    def test_get_nonexistent_knowledge(self):
        """Test retrieving nonexistent knowledge file."""
        data = self.memory_manager.get_knowledge("nonexistent.md")
        
        # Should return empty dict
        self.assertEqual(data, {})

    def test_add_execution_log(self):
        """Test adding execution log."""
        task_id = "task_123"
        log_data = {
            "task": "Test task",
            "status": "success",
            "timestamp": "2026-02-04T10:00:00"
        }
        
        # Add execution log
        self.memory_manager.add_execution_log(task_id, log_data)
        
        # Verify log was created
        log_path = Path(self.test_dir) / "working" / "execution_logs" / f"{task_id}.json"
        self.assertTrue(log_path.exists())
        
        # Verify log content
        with open(log_path, "r") as f:
            saved_log = json.load(f)
        self.assertEqual(saved_log, log_data)

    def test_working_memory_with_subdirectory(self):
        """Test working memory in subdirectory."""
        test_data = {"key": "value"}
        
        # Save to subdirectory
        self.memory_manager.save_working_memory("subdir/test.json", test_data)
        
        # Verify file was created in subdirectory
        file_path = Path(self.test_dir) / "working" / "subdir" / "test.json"
        self.assertTrue(file_path.parent.exists())

    def test_edge_case_complex_data_structure(self):
        """Test with complex nested data structure."""
        complex_data = {
            "level1": {
                "level2": {
                    "level3": ["item1", "item2", {"key": "value"}]
                }
            },
            "array": [1, 2, 3, 4, 5],
            "mixed": ["string", 123, True, None]
        }
        
        self.memory_manager.save_working_memory("complex.json", complex_data)
        retrieved_data = self.memory_manager.get_working_memory("complex.json")
        
        self.assertEqual(retrieved_data, complex_data)


if __name__ == "__main__":
    unittest.main()
