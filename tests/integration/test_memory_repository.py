"""Integration tests for memory repository and search functionality."""

import pytest
from pathlib import Path
import tempfile
import shutil

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository


@pytest.mark.integration
class TestFileMemoryRepository:
    """Integration tests for FileMemoryRepository."""
    
    @pytest.fixture
    def temp_memory_dir(self):
        """Create temporary directory for memory storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def repository(self, temp_memory_dir):
        """Create repository instance with temp directory."""
        return FileMemoryRepository(base_path=temp_memory_dir)
    
    @pytest.mark.asyncio
    async def test_save_and_retrieve_memory(self, repository):
        """Test saving and retrieving a memory."""
        memory = Memory(
            key="test_memory",
            type=MemoryType.WORKING,
            content={"data": "test_value"}
        )
        
        # Save memory
        await repository.save(memory)
        
        # Retrieve memory
        retrieved = await repository.get("test_memory")
        
        assert retrieved is not None
        assert retrieved.key == "test_memory"
        assert retrieved.content == {"data": "test_value"}
    
    @pytest.mark.asyncio
    async def test_list_memories_by_type(self, repository):
        """Test listing memories by type."""
        # Create multiple memories
        memory1 = Memory(key="working_1", type=MemoryType.WORKING, content={"data": "1"})
        memory2 = Memory(key="working_2", type=MemoryType.WORKING, content={"data": "2"})
        memory3 = Memory(key="knowledge_1", type=MemoryType.KNOWLEDGE, content={"data": "3"})
        
        await repository.save(memory1)
        await repository.save(memory2)
        await repository.save(memory3)
        
        # List working memories
        working_memories = await repository.list(MemoryType.WORKING)
        
        assert len(working_memories) == 2
        assert all(m.type == MemoryType.WORKING for m in working_memories)
    
    @pytest.mark.asyncio
    async def test_delete_memory(self, repository):
        """Test deleting a memory."""
        memory = Memory(
            key="delete_test",
            type=MemoryType.WORKING,
            content={"data": "delete_me"}
        )
        
        await repository.save(memory)
        
        # Verify it exists
        retrieved = await repository.get("delete_test")
        assert retrieved is not None
        
        # Delete it
        await repository.delete("delete_test")
        
        # Verify it's gone
        retrieved_after_delete = await repository.get("delete_test")
        assert retrieved_after_delete is None
    
    @pytest.mark.asyncio
    async def test_search_by_keywords(self, repository):
        """Test searching memories by keywords."""
        # Create memories with different content
        memory1 = Memory(
            key="search_1",
            type=MemoryType.KNOWLEDGE,
            content={"title": "Python Tutorial", "content": "Learn Python"}
        )
        memory2 = Memory(
            key="search_2",
            type=MemoryType.KNOWLEDGE,
            content={"title": "JavaScript Guide", "content": "Learn JavaScript"}
        )
        memory3 = Memory(
            key="search_3",
            type=MemoryType.KNOWLEDGE,
            content={"title": "Python Advanced", "content": "Advanced Python"}
        )
        
        await repository.save(memory1)
        await repository.save(memory2)
        await repository.save(memory3)
        
        # Search for "Python"
        results = await repository.search(
            memory_type=MemoryType.KNOWLEDGE,
            keywords=["Python"]
        )
        
        assert len(results) == 2
        assert all("Python" in str(m.content) for m in results)
    
    @pytest.mark.asyncio
    async def test_search_by_key_pattern(self, repository):
        """Test searching memories by key pattern."""
        memory1 = Memory(key="goal_2024_01", type=MemoryType.STRATEGIC, content={})
        memory2 = Memory(key="goal_2024_02", type=MemoryType.STRATEGIC, content={})
        memory3 = Memory(key="task_2024_01", type=MemoryType.WORKING, content={})
        
        await repository.save(memory1)
        await repository.save(memory2)
        await repository.save(memory3)
        
        # Search for keys containing "goal"
        results = await repository.search(key_pattern="goal")
        
        assert len(results) == 2
        assert all("goal" in m.key for m in results)
    
    @pytest.mark.asyncio
    async def test_search_by_tags(self, repository):
        """Test searching memories by tags."""
        memory1 = Memory(key="tagged_1", type=MemoryType.KNOWLEDGE, content={})
        memory1.add_tags(["python", "tutorial"])
        
        memory2 = Memory(key="tagged_2", type=MemoryType.KNOWLEDGE, content={})
        memory2.add_tags(["javascript", "tutorial"])
        
        memory3 = Memory(key="tagged_3", type=MemoryType.KNOWLEDGE, content={})
        memory3.add_tags(["python", "advanced"])
        
        await repository.save(memory1)
        await repository.save(memory2)
        await repository.save(memory3)
        
        # Search for python tag
        results = await repository.search(tags=["python"])
        
        assert len(results) == 2
        assert all(m.has_tag("python") for m in results)
    
    @pytest.mark.asyncio
    async def test_version_tracking(self, repository):
        """Test memory versioning."""
        memory = Memory(
            key="versioned_memory",
            type=MemoryType.KNOWLEDGE,
            content={"version": "1.0"}
        )
        
        # Save initial version
        await repository.save(memory)
        assert memory.get_version() == 1
        
        # Update content (increments version)
        memory.update_content({"version": "2.0"})
        await repository.save(memory)
        assert memory.get_version() == 2
        
        # Verify version history
        versions = await repository.list_versions("versioned_memory")
        assert len(versions) >= 2
        assert 1 in versions
        assert 2 in versions
    
    @pytest.mark.asyncio
    async def test_retrieve_specific_version(self, repository):
        """Test retrieving specific version of memory."""
        memory = Memory(
            key="version_test",
            type=MemoryType.KNOWLEDGE,
            content={"data": "v1"}
        )
        
        # Save version 1
        await repository.save(memory)
        
        # Update to version 2
        memory.update_content({"data": "v2"})
        await repository.save(memory)
        
        # Retrieve version 1
        v1_memory = await repository.get_by_version("version_test", 1)
        
        assert v1_memory is not None
        assert v1_memory.content["data"] == "v1"
        assert v1_memory.get_version() == 1
    
    @pytest.mark.asyncio
    async def test_search_pagination(self, repository):
        """Test search with pagination."""
        # Create many memories
        for i in range(15):
            memory = Memory(
                key=f"paginate_{i}",
                type=MemoryType.KNOWLEDGE,
                content={"index": i}
            )
            await repository.save(memory)
        
        # Get first page
        page1 = await repository.search(
            memory_type=MemoryType.KNOWLEDGE,
            limit=10,
            offset=0
        )
        
        # Get second page
        page2 = await repository.search(
            memory_type=MemoryType.KNOWLEDGE,
            limit=10,
            offset=10
        )
        
        assert len(page1) == 10
        assert len(page2) == 5
        
        # Ensure no overlap
        page1_keys = {m.key for m in page1}
        page2_keys = {m.key for m in page2}
        assert len(page1_keys & page2_keys) == 0
