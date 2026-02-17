"""Tests for cached memory repository."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.infrastructure.persistence.cached_memory_repository import CachedMemoryRepository
from jarvis_core.shared.constants import MemoryType


@pytest.mark.unit
class TestCachedMemoryRepository:
    """Test cases for CachedMemoryRepository."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock underlying repository."""
        mock = AsyncMock()
        return mock

    @pytest.fixture
    def cached_repo(self, mock_repository):
        """Create a cached repository with mock backend."""
        return CachedMemoryRepository(
            repository=mock_repository, cache_size=10, cache_ttl_seconds=60
        )

    @pytest.fixture
    def sample_memory(self):
        """Create a sample memory for testing."""
        return Memory(
            memory_id="mem_test123",
            type=MemoryType.WORKING,
            key="test_key",
            content={"data": "test"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={},
        )

    @pytest.mark.asyncio
    async def test_get_cache_miss(self, cached_repo, mock_repository, sample_memory):
        """Test cache miss on first get."""
        mock_repository.get.return_value = sample_memory

        result = await cached_repo.get("test_key")

        assert result == sample_memory
        mock_repository.get.assert_called_once_with("test_key")

        # Check stats
        stats = cached_repo.get_cache_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 1

    @pytest.mark.asyncio
    async def test_get_cache_hit(self, cached_repo, mock_repository, sample_memory):
        """Test cache hit on subsequent get."""
        mock_repository.get.return_value = sample_memory

        # First call - cache miss
        await cached_repo.get("test_key")

        # Second call - cache hit
        result = await cached_repo.get("test_key")

        assert result == sample_memory
        # Repository should only be called once
        assert mock_repository.get.call_count == 1

        # Check stats
        stats = cached_repo.get_cache_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1

    @pytest.mark.asyncio
    async def test_save_updates_cache(self, cached_repo, mock_repository, sample_memory):
        """Test that save updates the cache."""
        mock_repository.save.return_value = None

        await cached_repo.save(sample_memory)

        # Get should return cached value without calling repository
        mock_repository.get.return_value = sample_memory
        result = await cached_repo.get(sample_memory.key)

        assert result == sample_memory
        mock_repository.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_invalidates_cache(self, cached_repo, mock_repository, sample_memory):
        """Test that delete invalidates the cache."""
        mock_repository.get.return_value = sample_memory
        mock_repository.delete.return_value = None

        # Cache the memory
        await cached_repo.get("test_key")

        # Delete it
        await cached_repo.delete("test_key")

        # Get should now call repository again
        await cached_repo.get("test_key")

        # Repository get should be called twice (before and after delete)
        assert mock_repository.get.call_count == 2

    @pytest.mark.asyncio
    async def test_list_caching(self, cached_repo, mock_repository, sample_memory):
        """Test that list operations are cached."""
        mock_repository.list.return_value = [sample_memory]

        # First call
        result1 = await cached_repo.list(MemoryType.WORKING)

        # Second call - should be cached
        result2 = await cached_repo.list(MemoryType.WORKING)

        assert result1 == result2
        # Repository should only be called once
        mock_repository.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_invalidates_list_cache(self, cached_repo, mock_repository, sample_memory):
        """Test that save invalidates list cache."""
        mock_repository.list.return_value = [sample_memory]
        mock_repository.save.return_value = None

        # Cache the list
        await cached_repo.list(MemoryType.WORKING)

        # Save a new memory
        await cached_repo.save(sample_memory)

        # List again - should call repository again
        await cached_repo.list(MemoryType.WORKING)

        # Repository list should be called twice
        assert mock_repository.list.call_count == 2

    @pytest.mark.asyncio
    async def test_cache_eviction(self, mock_repository):
        """Test that cache evicts oldest entries when full."""
        cached_repo = CachedMemoryRepository(
            repository=mock_repository, cache_size=3, cache_ttl_seconds=60
        )

        # Add 4 memories (exceeding cache size of 3)
        for i in range(4):
            memory = Memory(
                memory_id=f"mem_{i}",
                type=MemoryType.WORKING,
                key=f"key_{i}",
                content={"data": f"test_{i}"},
            )
            mock_repository.get.return_value = memory
            await cached_repo.get(f"key_{i}")

        # Check that evictions occurred
        stats = cached_repo.get_cache_stats()
        assert stats["evictions"] > 0
        assert stats["cache_size"] <= 3

    @pytest.mark.asyncio
    async def test_cache_stats(self, cached_repo, mock_repository, sample_memory):
        """Test cache statistics tracking."""
        mock_repository.get.return_value = sample_memory

        # Perform some operations
        await cached_repo.get("test_key")  # miss
        await cached_repo.get("test_key")  # hit
        await cached_repo.get("other_key")  # miss

        stats = cached_repo.get_cache_stats()

        assert stats["hits"] == 1
        assert stats["misses"] == 2
        assert "hit_rate" in stats
        assert stats["cache_size"] == 2

    @pytest.mark.asyncio
    async def test_clear_cache(self, cached_repo, mock_repository, sample_memory):
        """Test clearing the cache."""
        mock_repository.get.return_value = sample_memory

        # Cache a memory
        await cached_repo.get("test_key")

        # Clear cache
        cached_repo.clear_cache()

        # Get should call repository again
        await cached_repo.get("test_key")

        assert mock_repository.get.call_count == 2

    @pytest.mark.asyncio
    async def test_pattern_search_bypasses_cache(self, cached_repo, mock_repository, sample_memory):
        """Test that pattern searches bypass cache."""
        mock_repository.get_by_type_and_pattern.return_value = [sample_memory]

        # Call twice
        await cached_repo.get_by_type_and_pattern(MemoryType.WORKING, "test")
        await cached_repo.get_by_type_and_pattern(MemoryType.WORKING, "test")

        # Should call repository both times (no caching)
        assert mock_repository.get_by_type_and_pattern.call_count == 2
