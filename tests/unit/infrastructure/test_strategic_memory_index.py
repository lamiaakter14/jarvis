"""Unit tests for strategic memory index."""

import shutil
import tempfile

import pytest
from jarvis_core.infrastructure.persistence.strategic_memory_index import StrategicMemoryIndex


@pytest.mark.unit
class TestStrategicMemoryIndex:
    """Test StrategicMemoryIndex functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for index storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def index(self, temp_dir):
        """Create index instance."""
        return StrategicMemoryIndex(base_path=temp_dir)

    def test_add_goal_entry(self, index):
        """Test adding a goal entry to the index."""
        index.add_entry(
            key="goal_123",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["strategic", "performance"],
        )

        # Verify entry in indexes
        assert "goal_123" in index.find_by_type("goal")
        assert "goal_123" in index.find_by_priority("high")
        assert "goal_123" in index.find_by_status("active")
        assert "goal_123" in index.find_by_tag("strategic")
        assert "goal_123" in index.find_by_tag("performance")

    def test_add_adr_entry(self, index):
        """Test adding an ADR entry to the index."""
        index.add_entry(
            key="adr_001",
            entry_type="adr",
            status="accepted",
            tags=["adr", "architecture", "database"],
        )

        # Verify entry in indexes
        assert "adr_001" in index.find_by_type("adr")
        assert "adr_001" in index.find_by_status("accepted")
        assert "adr_001" in index.find_by_tag("adr")
        assert "adr_001" in index.find_by_tag("architecture")
        assert "adr_001" in index.find_by_tag("database")

    def test_update_entry_priority(self, index):
        """Test updating entry priority."""
        # Add entry with low priority
        index.add_entry(
            key="goal_123", entry_type="goal", priority="low", status="active", tags=["test"]
        )

        assert "goal_123" in index.find_by_priority("low")
        assert "goal_123" not in index.find_by_priority("high")

        # Update to high priority
        index.add_entry(
            key="goal_123", entry_type="goal", priority="high", status="active", tags=["test"]
        )

        # Verify priority changed
        assert "goal_123" not in index.find_by_priority("low")
        assert "goal_123" in index.find_by_priority("high")

    def test_remove_entry(self, index):
        """Test removing an entry from the index."""
        # Add entry
        index.add_entry(
            key="goal_123", entry_type="goal", priority="high", status="active", tags=["test"]
        )

        assert "goal_123" in index.find_by_type("goal")

        # Remove entry
        index.remove_entry("goal_123")

        # Verify removed from all indexes
        assert "goal_123" not in index.find_by_type("goal")
        assert "goal_123" not in index.find_by_priority("high")
        assert "goal_123" not in index.find_by_status("active")
        assert "goal_123" not in index.find_by_tag("test")

    def test_find_by_tags_any(self, index):
        """Test finding entries by any of multiple tags."""
        # Add entries with different tags
        index.add_entry(
            key="goal_1",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "backend"],
        )
        index.add_entry(
            key="goal_2",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "frontend"],
        )
        index.add_entry(
            key="goal_3",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["security", "backend"],
        )

        # Search for performance OR security
        results = index.find_by_tags(["performance", "security"], match_all=False)

        assert len(results) == 3
        assert "goal_1" in results
        assert "goal_2" in results
        assert "goal_3" in results

    def test_find_by_tags_all(self, index):
        """Test finding entries by all of multiple tags."""
        # Add entries with different tags
        index.add_entry(
            key="goal_1",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "backend"],
        )
        index.add_entry(
            key="goal_2",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "frontend"],
        )
        index.add_entry(
            key="goal_3",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["security", "backend"],
        )

        # Search for performance AND backend
        results = index.find_by_tags(["performance", "backend"], match_all=True)

        assert len(results) == 1
        assert "goal_1" in results

    def test_get_metadata(self, index):
        """Test getting metadata for an entry."""
        index.add_entry(
            key="goal_123", entry_type="goal", priority="high", status="active", tags=["test"]
        )

        metadata = index.get_metadata("goal_123")

        assert metadata is not None
        assert metadata["type"] == "goal"
        assert metadata["priority"] == "high"
        assert metadata["status"] == "active"
        assert "test" in metadata["tags"]

    def test_get_statistics(self, index):
        """Test getting index statistics."""
        # Add multiple entries
        index.add_entry(
            key="goal_1", entry_type="goal", priority="high", status="active", tags=["performance"]
        )
        index.add_entry(
            key="goal_2",
            entry_type="goal",
            priority="medium",
            status="active",
            tags=["performance", "backend"],
        )
        index.add_entry(
            key="adr_1", entry_type="adr", status="accepted", tags=["adr", "architecture"]
        )

        stats = index.get_statistics()

        assert stats["total_entries"] == 3
        assert stats["by_type"]["goal"] == 2
        assert stats["by_type"]["adr"] == 1
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["medium"] == 1
        assert stats["by_status"]["active"] == 2
        assert stats["by_status"]["accepted"] == 1

    def test_persistence(self, temp_dir):
        """Test that index persists across instances."""
        # Create first index and add entries
        index1 = StrategicMemoryIndex(base_path=temp_dir)
        index1.add_entry(
            key="goal_123", entry_type="goal", priority="high", status="active", tags=["test"]
        )

        # Create new index instance (should load persisted data)
        index2 = StrategicMemoryIndex(base_path=temp_dir)

        # Verify data was persisted
        assert "goal_123" in index2.find_by_type("goal")
        assert "goal_123" in index2.find_by_priority("high")
        assert "goal_123" in index2.find_by_tag("test")

    def test_get_all_tags(self, index):
        """Test getting all unique tags."""
        index.add_entry(
            key="goal_1",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "backend"],
        )
        index.add_entry(
            key="goal_2",
            entry_type="goal",
            priority="high",
            status="active",
            tags=["performance", "frontend"],
        )

        all_tags = index.get_all_tags()

        assert "performance" in all_tags
        assert "backend" in all_tags
        assert "frontend" in all_tags
