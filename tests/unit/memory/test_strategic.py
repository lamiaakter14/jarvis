"""Unit tests for strategic memory module."""

import pytest
import tempfile
import os

from jarvis_core.memory.strategic import (
    StrategicMemoryStore,
    store_goal_snapshot,
    trajectory_delta
)
from jarvis_core.shared.exceptions import RepositoryError


@pytest.mark.unit
class TestStrategicMemoryStore:
    """Test strategic memory store functionality."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database path for testing."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            db_path = f.name
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
    
    @pytest.fixture
    def store(self, temp_db_path):
        """Create a strategic memory store for testing."""
        return StrategicMemoryStore(db_path=temp_db_path)
    
    def test_store_initialization(self, store):
        """Test that store initializes correctly."""
        assert store is not None
        assert store.db_path.exists()
    
    def test_store_goal_snapshot(self, store):
        """Test storing a goal snapshot."""
        snapshot = {
            "goal_id": "goal_001",
            "title": "Test goal",
            "progress": 0.5,
            "status": "in_progress"
        }
        
        snapshot_id = store.store_snapshot(snapshot)
        assert snapshot_id > 0
    
    def test_store_empty_snapshot_raises_error(self, store):
        """Test that empty snapshot raises ValueError."""
        with pytest.raises(ValueError, match="Goal snapshot cannot be empty"):
            store.store_snapshot({})
    
    def test_store_non_dict_snapshot_raises_error(self, store):
        """Test that non-dict snapshot raises ValueError."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            store.store_snapshot("not a dict")
    
    def test_store_snapshot_without_goal_id_raises_error(self, store):
        """Test that snapshot without goal_id raises ValueError."""
        with pytest.raises(ValueError, match="must contain 'goal_id' field"):
            store.store_snapshot({"title": "Test"})
    
    def test_retrieve_latest_snapshot(self, store):
        """Test retrieving the latest snapshot."""
        snapshot = {
            "goal_id": "goal_001",
            "title": "Test goal",
            "progress": 0.5
        }
        
        store.store_snapshot(snapshot)
        
        retrieved = store.get_latest_snapshot("goal_001")
        assert retrieved is not None
        assert retrieved["goal_id"] == "goal_001"
        assert retrieved["title"] == "Test goal"
        assert retrieved["progress"] == 0.5
        assert "_created_at" in retrieved
        assert "_version" in retrieved
        assert retrieved["_version"] == 1
    
    def test_retrieve_nonexistent_goal_returns_none(self, store):
        """Test retrieving non-existent goal returns None."""
        retrieved = store.get_latest_snapshot("nonexistent")
        assert retrieved is None
    
    def test_snapshot_versioning(self, store):
        """Test that snapshots are versioned correctly."""
        goal_id = "goal_001"
        
        # Store first version
        snapshot_v1 = {"goal_id": goal_id, "progress": 0.3}
        store.store_snapshot(snapshot_v1)
        
        # Store second version
        snapshot_v2 = {"goal_id": goal_id, "progress": 0.6}
        store.store_snapshot(snapshot_v2)
        
        # Store third version
        snapshot_v3 = {"goal_id": goal_id, "progress": 0.9}
        store.store_snapshot(snapshot_v3)
        
        # Latest should be version 3
        latest = store.get_latest_snapshot(goal_id)
        assert latest["_version"] == 3
        assert latest["progress"] == 0.9
    
    def test_get_snapshot_history(self, store):
        """Test retrieving snapshot history."""
        goal_id = "goal_001"
        
        # Store multiple versions
        for i in range(5):
            snapshot = {"goal_id": goal_id, "progress": i * 0.2}
            store.store_snapshot(snapshot)
        
        history = store.get_snapshot_history(goal_id, limit=3)
        
        assert len(history) == 3
        # Should be in descending version order
        assert history[0]["_version"] == 5
        assert history[1]["_version"] == 4
        assert history[2]["_version"] == 3
    
    def test_get_snapshot_history_empty(self, store):
        """Test getting history for non-existent goal."""
        history = store.get_snapshot_history("nonexistent")
        assert history == []


@pytest.mark.unit
class TestTrajectoryDelta:
    """Test trajectory delta calculation."""
    
    def test_delta_with_added_fields(self):
        """Test delta calculation when fields are added."""
        prev = {"goal_id": "g1", "progress": 0.3}
        curr = {"goal_id": "g1", "progress": 0.3, "notes": "Added notes"}
        
        delta = trajectory_delta(prev, curr)
        
        assert delta["added"] == {"notes": "Added notes"}
        assert delta["removed"] == {}
        assert delta["modified"] == {}
        assert delta["unchanged"] == {"goal_id": "g1", "progress": 0.3}
        assert delta["has_changes"] is True
    
    def test_delta_with_removed_fields(self):
        """Test delta calculation when fields are removed."""
        prev = {"goal_id": "g1", "progress": 0.3, "notes": "Old notes"}
        curr = {"goal_id": "g1", "progress": 0.3}
        
        delta = trajectory_delta(prev, curr)
        
        assert delta["added"] == {}
        assert delta["removed"] == {"notes": "Old notes"}
        assert delta["modified"] == {}
        assert delta["unchanged"] == {"goal_id": "g1", "progress": 0.3}
        assert delta["has_changes"] is True
    
    def test_delta_with_modified_fields(self):
        """Test delta calculation when fields are modified."""
        prev = {"goal_id": "g1", "progress": 0.3, "status": "pending"}
        curr = {"goal_id": "g1", "progress": 0.6, "status": "in_progress"}
        
        delta = trajectory_delta(prev, curr)
        
        assert delta["added"] == {}
        assert delta["removed"] == {}
        assert delta["modified"] == {
            "progress": {"old": 0.3, "new": 0.6},
            "status": {"old": "pending", "new": "in_progress"}
        }
        assert delta["unchanged"] == {"goal_id": "g1"}
        assert delta["has_changes"] is True
    
    def test_delta_with_no_changes(self):
        """Test delta calculation when nothing changes."""
        prev = {"goal_id": "g1", "progress": 0.5}
        curr = {"goal_id": "g1", "progress": 0.5}
        
        delta = trajectory_delta(prev, curr)
        
        assert delta["added"] == {}
        assert delta["removed"] == {}
        assert delta["modified"] == {}
        assert delta["unchanged"] == {"goal_id": "g1", "progress": 0.5}
        assert delta["has_changes"] is False
    
    def test_delta_ignores_metadata_fields(self):
        """Test that delta ignores fields starting with underscore."""
        prev = {"goal_id": "g1", "progress": 0.3, "_created_at": "2024-01-01"}
        curr = {"goal_id": "g1", "progress": 0.6, "_created_at": "2024-01-02"}
        
        delta = trajectory_delta(prev, curr)
        
        # _created_at should not appear in any category
        assert "_created_at" not in delta["added"]
        assert "_created_at" not in delta["removed"]
        assert "_created_at" not in delta["modified"]
        assert "_created_at" not in delta["unchanged"]
    
    def test_delta_with_complex_values(self):
        """Test delta with nested structures."""
        prev = {
            "goal_id": "g1",
            "tasks": ["task1", "task2"],
            "metadata": {"priority": "high"}
        }
        curr = {
            "goal_id": "g1",
            "tasks": ["task1", "task2", "task3"],
            "metadata": {"priority": "critical"}
        }
        
        delta = trajectory_delta(prev, curr)
        
        assert delta["modified"]["tasks"]["old"] == ["task1", "task2"]
        assert delta["modified"]["tasks"]["new"] == ["task1", "task2", "task3"]
        assert delta["modified"]["metadata"]["old"] == {"priority": "high"}
        assert delta["modified"]["metadata"]["new"] == {"priority": "critical"}
    
    def test_delta_invalid_input_raises_error(self):
        """Test that invalid inputs raise ValueError."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            trajectory_delta("not a dict", {})
        
        with pytest.raises(ValueError, match="must be a dictionary"):
            trajectory_delta({}, "not a dict")


@pytest.mark.unit
class TestStrategicModuleFunctions:
    """Test module-level functions."""
    
    def test_store_goal_snapshot_function(self):
        """Test store_goal_snapshot function."""
        import jarvis_core.memory.strategic as strategic_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            strategic_module._store = StrategicMemoryStore(db_path=db_path)
            
            snapshot = {
                "goal_id": "goal_001",
                "title": "Test goal",
                "progress": 0.5
            }
            
            snapshot_id = store_goal_snapshot(snapshot)
            assert snapshot_id > 0
            
            # Reset global store
            strategic_module._store = None
