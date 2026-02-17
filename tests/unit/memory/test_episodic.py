"""Unit tests for episodic memory module."""

import pytest
import tempfile
import os
from datetime import datetime, timedelta

from jarvis_core.memory.episodic import (
    EpisodicMemoryStore,
    store_daily_log,
    retrieve_last_n_days
)
from jarvis_core.shared.exceptions import RepositoryError


@pytest.mark.unit
class TestEpisodicMemoryStore:
    """Test episodic memory store functionality."""
    
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
        """Create an episodic memory store for testing."""
        return EpisodicMemoryStore(db_path=temp_db_path)
    
    def test_store_initialization(self, store):
        """Test that store initializes correctly."""
        assert store is not None
        assert store.db_path.exists()
    
    def test_store_single_entry(self, store):
        """Test storing a single log entry."""
        entries = ["Test log entry"]
        store.store_entries(entries)
        
        # Retrieve and verify
        logs = store.retrieve_last_n_days(1)
        assert len(logs) == 1
        assert logs[0]["entry"] == "Test log entry"
    
    def test_store_multiple_entries(self, store):
        """Test storing multiple log entries."""
        entries = ["Entry 1", "Entry 2", "Entry 3"]
        store.store_entries(entries)
        
        logs = store.retrieve_last_n_days(1)
        assert len(logs) == 3
        entries_retrieved = [log["entry"] for log in logs]
        assert set(entries_retrieved) == set(entries)
    
    def test_store_empty_list_raises_error(self, store):
        """Test that storing an empty list raises ValueError."""
        with pytest.raises(ValueError, match="Entries list cannot be empty"):
            store.store_entries([])
    
    def test_store_non_string_entries_raises_error(self, store):
        """Test that non-string entries raise ValueError."""
        with pytest.raises(ValueError, match="All entries must be strings"):
            store.store_entries([123, "valid"])
    
    def test_store_filters_empty_strings(self, store):
        """Test that empty strings are filtered out."""
        entries = ["Valid entry", "   ", "", "Another entry"]
        store.store_entries(entries)
        
        logs = store.retrieve_last_n_days(1)
        assert len(logs) == 2
        entries_retrieved = [log["entry"] for log in logs]
        assert "Valid entry" in entries_retrieved
        assert "Another entry" in entries_retrieved
    
    def test_store_all_empty_raises_error(self, store):
        """Test that all empty entries raises ValueError."""
        with pytest.raises(ValueError, match="No valid entries to store"):
            store.store_entries(["", "   ", ""])
    
    def test_retrieve_last_n_days(self, store):
        """Test retrieving logs from last n days."""
        entries = ["Day 1 entry"]
        store.store_entries(entries)
        
        logs = store.retrieve_last_n_days(7)
        assert len(logs) >= 1
        assert logs[0]["entry"] == "Day 1 entry"
    
    def test_retrieve_invalid_days_raises_error(self, store):
        """Test that invalid day count raises ValueError."""
        with pytest.raises(ValueError, match="must be a positive integer"):
            store.retrieve_last_n_days(0)
        
        with pytest.raises(ValueError, match="must be a positive integer"):
            store.retrieve_last_n_days(-1)
        
        with pytest.raises(ValueError, match="must be a positive integer"):
            store.retrieve_last_n_days("invalid")
    
    def test_retrieve_returns_empty_for_no_logs(self, store):
        """Test that retrieval returns empty list when no logs exist."""
        logs = store.retrieve_last_n_days(7)
        assert logs == []
    
    def test_log_includes_metadata(self, store):
        """Test that retrieved logs include necessary metadata."""
        entries = ["Test entry"]
        store.store_entries(entries)
        
        logs = store.retrieve_last_n_days(1)
        assert len(logs) == 1
        log = logs[0]
        
        assert "id" in log
        assert "entry" in log
        assert "created_at" in log
        assert "log_date" in log
        
        # Verify date format
        datetime.fromisoformat(log["created_at"])
        datetime.fromisoformat(log["log_date"]).date()


@pytest.mark.unit
class TestEpisodicModuleFunctions:
    """Test module-level functions."""
    
    def test_store_daily_log(self):
        """Test store_daily_log function."""
        # Use a temporary database
        import jarvis_core.memory.episodic as episodic_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            episodic_module._store = EpisodicMemoryStore(db_path=db_path)
            
            entries = ["Test entry 1", "Test entry 2"]
            store_daily_log(entries)
            
            logs = retrieve_last_n_days(1)
            assert len(logs) == 2
            
            # Reset global store
            episodic_module._store = None
    
    def test_retrieve_last_n_days_function(self):
        """Test retrieve_last_n_days function."""
        import jarvis_core.memory.episodic as episodic_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            episodic_module._store = EpisodicMemoryStore(db_path=db_path)
            
            # Store some entries
            store_daily_log(["Entry 1", "Entry 2"])
            
            # Retrieve
            logs = retrieve_last_n_days(3)
            assert len(logs) == 2
            
            # Reset global store
            episodic_module._store = None
