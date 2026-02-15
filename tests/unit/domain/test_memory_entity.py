"""Unit tests for Memory entity enhancements."""

import pytest
from datetime import datetime

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException


@pytest.mark.unit
class TestMemoryVersioning:
    """Test memory versioning functionality."""
    
    def test_memory_initializes_with_version_1(self):
        """Test that new memory starts with version 1."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        assert memory.get_version() == 1
        assert memory.metadata["version"] == 1
    
    def test_memory_preserves_existing_version(self):
        """Test that existing version is preserved."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"},
            metadata={"version": 5}
        )
        
        assert memory.get_version() == 5
    
    def test_update_content_increments_version(self):
        """Test that updating content increments version."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        initial_version = memory.get_version()
        memory.update_content({"data": "updated"})
        
        assert memory.get_version() == initial_version + 1
        assert memory.content["data"] == "updated"
    
    def test_update_content_without_version_increment(self):
        """Test updating content without incrementing version."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        initial_version = memory.get_version()
        memory.update_content({"data": "updated"}, increment_version=False)
        
        assert memory.get_version() == initial_version
        assert memory.content["data"] == "updated"
    
    def test_set_version(self):
        """Test manually setting version."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        memory.set_version(10)
        
        assert memory.get_version() == 10
    
    def test_set_version_validates_minimum(self):
        """Test that version must be at least 1."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        with pytest.raises(DomainException, match="Version must be at least 1"):
            memory.set_version(0)
        
        with pytest.raises(DomainException, match="Version must be at least 1"):
            memory.set_version(-1)


@pytest.mark.unit
class TestMemoryTags:
    """Test memory tagging functionality."""
    
    def test_add_tags_to_memory(self):
        """Test adding tags to memory."""
        memory = Memory(
            key="test_key",
            type=MemoryType.KNOWLEDGE,
            content={"data": "test"}
        )
        
        memory.add_tags(["important", "urgent"])
        
        assert "important" in memory.get_tags()
        assert "urgent" in memory.get_tags()
    
    def test_add_tags_prevents_duplicates(self):
        """Test that duplicate tags are not added."""
        memory = Memory(
            key="test_key",
            type=MemoryType.KNOWLEDGE,
            content={"data": "test"}
        )
        
        memory.add_tags(["tag1", "tag2"])
        memory.add_tags(["tag2", "tag3"])
        
        tags = memory.get_tags()
        assert tags.count("tag2") == 1
        assert "tag1" in tags
        assert "tag3" in tags
    
    def test_has_tag(self):
        """Test checking if memory has a specific tag."""
        memory = Memory(
            key="test_key",
            type=MemoryType.KNOWLEDGE,
            content={"data": "test"}
        )
        
        memory.add_tags(["test", "sample"])
        
        assert memory.has_tag("test") is True
        assert memory.has_tag("sample") is True
        assert memory.has_tag("nonexistent") is False
    
    def test_get_tags_empty(self):
        """Test getting tags when none exist."""
        memory = Memory(
            key="test_key",
            type=MemoryType.KNOWLEDGE,
            content={"data": "test"}
        )
        
        tags = memory.get_tags()
        
        assert tags == []
    
    def test_add_empty_tags(self):
        """Test that empty tags are not added."""
        memory = Memory(
            key="test_key",
            type=MemoryType.KNOWLEDGE,
            content={"data": "test"}
        )
        
        memory.add_tags(["tag1", "", "tag2"])
        
        tags = memory.get_tags()
        assert "tag1" in tags
        assert "tag2" in tags
        assert "" not in tags


@pytest.mark.unit
class TestMemoryRepresentation:
    """Test memory string representation with versioning."""
    
    def test_repr_includes_version(self):
        """Test that __repr__ includes version information."""
        memory = Memory(
            key="test_key",
            type=MemoryType.WORKING,
            content={"data": "test"}
        )
        
        memory.set_version(3)
        
        repr_str = repr(memory)
        
        assert "version=3" in repr_str
        assert "test_key" in repr_str
