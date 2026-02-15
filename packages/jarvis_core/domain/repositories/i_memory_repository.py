"""Memory repository interface for the domain layer."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType


class IMemoryRepository(ABC):
    """Abstract interface for memory persistence operations.
    
    This interface defines the contract for storing and retrieving memories
    in the JARVIS system. Implementations handle the actual persistence
    mechanism (e.g., file system, database, cache).
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Memory]:
        """Retrieve a memory by its key.
        
        Args:
            key: Unique key identifying the memory
            
        Returns:
            Memory instance if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        pass
    
    @abstractmethod
    async def save(self, memory: Memory) -> None:
        """Persist a memory to storage.
        
        Args:
            memory: Memory instance to save
            
        Raises:
            RepositoryError: If save operation fails
            ValidationError: If memory data is invalid
        """
        pass
    
    @abstractmethod
    async def list(self, memory_type: MemoryType) -> List[Memory]:
        """List all memories of a specific type.
        
        Args:
            memory_type: Type of memories to retrieve
            
        Returns:
            List of Memory instances matching the type
            
        Raises:
            RepositoryError: If list operation fails
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a memory by its key.
        
        Args:
            key: Unique key identifying the memory to delete
            
        Raises:
            RepositoryError: If delete operation fails
            EntityNotFoundError: If memory with key does not exist
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        memory_type: Optional[MemoryType] = None,
        keywords: Optional[List[str]] = None,
        key_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Memory]:
        """Search for memories based on multiple criteria.
        
        Args:
            memory_type: Filter by memory type
            keywords: Keywords to search for in content
            key_pattern: Pattern to match in keys
            tags: Tags to filter by
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of matching Memory instances
            
        Raises:
            RepositoryError: If search operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_version(self, key: str, version: int) -> Optional[Memory]:
        """Retrieve a specific version of a memory.
        
        Args:
            key: Memory key
            version: Version number to retrieve
            
        Returns:
            Memory instance if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        pass
    
    @abstractmethod
    async def list_versions(self, key: str) -> List[int]:
        """List all available versions of a memory.
        
        Args:
            key: Memory key
            
        Returns:
            List of version numbers
            
        Raises:
            RepositoryError: If list operation fails
        """
        pass
