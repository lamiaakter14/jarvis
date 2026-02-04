"""Memory repository interface for the domain layer."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.memory import Memory
from src.shared.constants import MemoryType


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
            RepositoryException: If retrieval operation fails
        """
        pass
    
    @abstractmethod
    async def save(self, memory: Memory) -> None:
        """Persist a memory to storage.
        
        Args:
            memory: Memory instance to save
            
        Raises:
            RepositoryException: If save operation fails
            ValidationException: If memory data is invalid
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
            RepositoryException: If list operation fails
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a memory by its key.
        
        Args:
            key: Unique key identifying the memory to delete
            
        Raises:
            RepositoryException: If delete operation fails
            NotFoundException: If memory with key does not exist
        """
        pass
