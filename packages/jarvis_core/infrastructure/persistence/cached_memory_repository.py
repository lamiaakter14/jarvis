"""Cached memory repository with LRU caching for performance optimization."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType


class CachedMemoryRepository(IMemoryRepository):
    """Wrapper repository that adds LRU caching to memory operations.
    
    This implementation provides:
    - LRU cache for frequently accessed memories
    - Time-based cache invalidation
    - Cache statistics for monitoring
    - Write-through caching strategy
    
    Performance target: <500ms for cached queries
    """
    
    def __init__(
        self,
        repository: IMemoryRepository,
        cache_size: int = 128,
        cache_ttl_seconds: int = 300
    ):
        """Initialize cached memory repository.
        
        Args:
            repository: Underlying repository implementation
            cache_size: Maximum number of cached entries (default: 128)
            cache_ttl_seconds: Cache time-to-live in seconds (default: 300)
        """
        self._repository = repository
        self._cache_size = cache_size
        self._cache_ttl = timedelta(seconds=cache_ttl_seconds)
        
        # Cache for individual memory lookups (key -> (memory, timestamp))
        self._memory_cache: Dict[str, tuple[Memory, datetime]] = {}
        
        # Cache for list operations (memory_type -> (list, timestamp))
        self._list_cache: Dict[MemoryType, tuple[List[Memory], datetime]] = {}
        
        # Cache statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "invalidations": 0,
            "evictions": 0
        }
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cached data is still valid.
        
        Args:
            timestamp: Timestamp when data was cached
            
        Returns:
            True if cache is still valid, False otherwise
        """
        return datetime.now() - timestamp < self._cache_ttl
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache size exceeds limit."""
        if len(self._memory_cache) > self._cache_size:
            # Sort by timestamp and remove oldest entries
            sorted_items = sorted(
                self._memory_cache.items(),
                key=lambda x: x[1][1]
            )
            num_to_remove = len(self._memory_cache) - self._cache_size
            for key, _ in sorted_items[:num_to_remove]:
                del self._memory_cache[key]
                self._stats["evictions"] += 1
    
    def _invalidate_cache(self, key: Optional[str] = None) -> None:
        """Invalidate cache entries.
        
        Args:
            key: Specific key to invalidate, or None to invalidate all
        """
        if key:
            if key in self._memory_cache:
                del self._memory_cache[key]
                self._stats["invalidations"] += 1
        else:
            # Invalidate all caches
            self._memory_cache.clear()
            self._list_cache.clear()
            self._stats["invalidations"] += 1
    
    async def get(self, key: str) -> Optional[Memory]:
        """Retrieve a memory by its key (with caching).
        
        Args:
            key: Unique key identifying the memory
            
        Returns:
            Memory instance if found, None otherwise
        """
        # Check cache first
        if key in self._memory_cache:
            memory, timestamp = self._memory_cache[key]
            if self._is_cache_valid(timestamp):
                self._stats["hits"] += 1
                return memory
            else:
                # Expired cache entry
                del self._memory_cache[key]
        
        # Cache miss - fetch from underlying repository
        self._stats["misses"] += 1
        memory = await self._repository.get(key)
        
        if memory:
            # Cache the result
            self._memory_cache[key] = (memory, datetime.now())
            self._evict_if_needed()
        
        return memory
    
    async def save(self, memory: Memory) -> None:
        """Persist a memory to storage (write-through cache).
        
        Args:
            memory: Memory instance to save
        """
        # Save to underlying repository
        await self._repository.save(memory)
        
        # Update cache (write-through)
        self._memory_cache[memory.key] = (memory, datetime.now())
        self._evict_if_needed()
        
        # Invalidate list cache as it's now stale
        self._list_cache.clear()
    
    async def list(self, memory_type: MemoryType) -> List[Memory]:
        """List all memories of a specific type (with caching).
        
        Args:
            memory_type: Type of memories to retrieve
            
        Returns:
            List of Memory instances matching the type
        """
        # Check list cache
        if memory_type in self._list_cache:
            memories, timestamp = self._list_cache[memory_type]
            if self._is_cache_valid(timestamp):
                self._stats["hits"] += 1
                return memories
            else:
                # Expired cache entry
                del self._list_cache[memory_type]
        
        # Cache miss - fetch from underlying repository
        self._stats["misses"] += 1
        memories = await self._repository.list(memory_type)
        
        # Cache the result
        self._list_cache[memory_type] = (memories, datetime.now())
        
        return memories
    
    async def delete(self, key: str) -> None:
        """Delete a memory by its key.
        
        Args:
            key: Unique key identifying the memory
        """
        # Delete from underlying repository
        await self._repository.delete(key)
        
        # Invalidate cache
        self._invalidate_cache(key)
        self._list_cache.clear()
    
    async def get_by_type_and_pattern(
        self,
        memory_type: MemoryType,
        key_pattern: str
    ) -> List[Memory]:
        """Get memories by type that match a key pattern.
        
        Note: Pattern-based queries are not cached as they vary too much.
        
        Args:
            memory_type: Memory type to filter by
            key_pattern: Pattern to match in keys
            
        Returns:
            List of matching memories
        """
        # Pattern queries bypass cache due to high variability
        return await self._repository.get_by_type_and_pattern(
            memory_type,
            key_pattern
        )
    
    async def search(
        self,
        memory_type: Optional[MemoryType] = None,
        keywords: Optional[List[str]] = None,
        key_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Memory]:
        """Search memories with filters.
        
        Note: Complex search queries are not cached.
        
        Args:
            memory_type: Optional memory type filter
            keywords: Optional content search keywords
            key_pattern: Optional key pattern to match
            tags: Optional tags to filter by
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of matching memories
        """
        # Complex search queries bypass cache
        return await self._repository.search(
            memory_type=memory_type,
            keywords=keywords,
            key_pattern=key_pattern,
            tags=tags,
            limit=limit,
            offset=offset
        )
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = (
            self._stats["hits"] / total_requests * 100
            if total_requests > 0
            else 0
        )
        
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": f"{hit_rate:.2f}%",
            "invalidations": self._stats["invalidations"],
            "evictions": self._stats["evictions"],
            "cache_size": len(self._memory_cache),
            "list_cache_size": len(self._list_cache),
            "max_cache_size": self._cache_size,
            "cache_ttl_seconds": self._cache_ttl.total_seconds()
        }
    
    def clear_cache(self) -> None:
        """Clear all cache entries."""
        self._memory_cache.clear()
        self._list_cache.clear()
