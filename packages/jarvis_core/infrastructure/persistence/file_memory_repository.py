"""File-based memory repository implementation."""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json

from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import RepositoryError, EntityNotFoundError
from jarvis_core.infrastructure.persistence.json_storage import JsonStorage
from jarvis_core.infrastructure.persistence.strategic_memory_index import StrategicMemoryIndex


class FileMemoryRepository(IMemoryRepository):
    """File-based implementation of memory repository.
    
    Stores memories as JSON files organized by memory type in the
    file system, maintaining compatibility with the existing memory structure.
    Includes indexed storage for strategic memory for fast retrieval.
    """
    
    def __init__(self, base_path: str = "memory"):
        """Initialize file memory repository.
        
        Args:
            base_path: Base directory for memory storage
        """
        self.storage = JsonStorage(base_path)
        self.strategic_index = StrategicMemoryIndex(base_path)
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required memory directories exist."""
        for memory_type in MemoryType:
            dir_name = self._get_directory_name(memory_type)
            self.storage.ensure_directory(dir_name)
    
    def _get_directory_name(self, memory_type: MemoryType) -> str:
        """Get directory name for a memory type.
        
        Args:
            memory_type: Memory type
            
        Returns:
            Directory name
        """
        type_mapping = {
            MemoryType.WORKING: "working",
            MemoryType.KNOWLEDGE: "knowledge",
            MemoryType.STRATEGIC: "strategic",
            MemoryType.EXECUTION_LOG: "working/execution_logs",
        }
        return type_mapping.get(memory_type, "working")
    
    def _get_file_path(self, memory_type: MemoryType, key: str) -> str:
        """Get file path for a memory.
        
        Args:
            memory_type: Memory type
            key: Memory key
            
        Returns:
            Relative file path
        """
        dir_name = self._get_directory_name(memory_type)
        # Sanitize key to create safe filename
        safe_key = key.replace("/", "_").replace("\\", "_")
        return f"{dir_name}/{safe_key}.json"
    
    def _memory_to_dict(self, memory: Memory) -> dict:
        """Convert Memory entity to dictionary for storage.
        
        Args:
            memory: Memory entity
            
        Returns:
            Dictionary representation
        """
        return {
            "memory_id": memory.memory_id,
            "type": memory.type.value,
            "key": memory.key,
            "content": memory.content,
            "created_at": memory.created_at.isoformat(),
            "updated_at": memory.updated_at.isoformat(),
            "metadata": memory.metadata,
        }
    
    def _dict_to_memory(self, data: dict) -> Memory:
        """Convert dictionary to Memory entity.
        
        Args:
            data: Dictionary with memory data
            
        Returns:
            Memory entity
            
        Raises:
            RepositoryError: If data is invalid
        """
        from datetime import datetime
        
        try:
            return Memory(
                memory_id=data["memory_id"],
                type=MemoryType(data["type"]),
                key=data["key"],
                content=data["content"],
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"]),
                metadata=data.get("metadata", {}),
            )
        except Exception as e:
            raise RepositoryError(f"Failed to deserialize memory: {e}")
    
    async def get(self, key: str) -> Optional[Memory]:
        """Retrieve a memory by its key.
        
        Args:
            key: Unique key identifying the memory
            
        Returns:
            Memory instance if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        try:
            # Try to find the memory in all memory type directories
            for memory_type in MemoryType:
                file_path = self._get_file_path(memory_type, key)
                if self.storage.exists(file_path):
                    data = self.storage.load(file_path)
                    return self._dict_to_memory(data)
            
            return None
        except Exception as e:
            raise RepositoryError(f"Failed to get memory '{key}': {e}")
    
    async def save(self, memory: Memory) -> None:
        """Persist a memory to storage.
        
        Args:
            memory: Memory instance to save
            
        Raises:
            RepositoryError: If save operation fails
        """
        try:
            file_path = self._get_file_path(memory.type, memory.key)
            data = self._memory_to_dict(memory)
            self.storage.save(file_path, data)
            
            # Save version history
            await self._save_version(memory)
            
            # Update strategic memory index if applicable
            if memory.type == MemoryType.STRATEGIC:
                self._update_strategic_index(memory)
            
        except Exception as e:
            raise RepositoryError(f"Failed to save memory '{memory.key}': {e}")
    
    async def list(self, memory_type: MemoryType) -> List[Memory]:
        """List all memories of a specific type.
        
        Args:
            memory_type: Type of memories to retrieve
            
        Returns:
            List of Memory instances matching the type
            
        Raises:
            RepositoryError: If list operation fails
        """
        try:
            memories = []
            dir_name = self._get_directory_name(memory_type)
            dir_path = self.storage.get_full_path(dir_name)
            
            if not dir_path.exists():
                return memories
            
            # Find all JSON files in the directory
            for file_path in dir_path.glob("*.json"):
                try:
                    data = self.storage.load(str(file_path.relative_to(self.storage.base_path)))
                    memory = self._dict_to_memory(data)
                    
                    # Verify memory type matches
                    if memory.type == memory_type:
                        memories.append(memory)
                except Exception as e:
                    # Log error but continue processing other files
                    print(f"Warning: Failed to load memory from {file_path}: {e}")
                    continue
            
            return memories
        except Exception as e:
            raise RepositoryError(f"Failed to list memories of type '{memory_type.value}': {e}")
    
    async def delete(self, key: str) -> None:
        """Delete a memory by its key.
        
        Args:
            key: Unique key identifying the memory to delete
            
        Raises:
            RepositoryError: If delete operation fails
            EntityNotFoundError: If memory with key does not exist
        """
        try:
            # Try to find and delete the memory in all memory type directories
            found = False
            found_type = None
            for memory_type in MemoryType:
                file_path = self._get_file_path(memory_type, key)
                if self.storage.exists(file_path):
                    self.storage.delete(file_path)
                    found = True
                    found_type = memory_type
                    break
            
            if not found:
                raise EntityNotFoundError(f"Memory with key '{key}' not found")
            
            # Remove from strategic index if applicable
            if found_type == MemoryType.STRATEGIC:
                self.strategic_index.remove_entry(key)
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise RepositoryError(f"Failed to delete memory '{key}': {e}")
    
    async def get_by_type_and_pattern(
        self,
        memory_type: MemoryType,
        key_pattern: str
    ) -> List[Memory]:
        """Get memories by type that match a key pattern.
        
        Args:
            memory_type: Memory type to filter by
            key_pattern: Pattern to match in keys (simple contains check)
            
        Returns:
            List of matching memories
        """
        all_memories = await self.list(memory_type)
        return [m for m in all_memories if key_pattern in m.key]
    
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
        
        Uses indexed storage for strategic memory searches to improve performance.
        
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
        try:
            # Use index for strategic memory when filtering by tags
            if memory_type == MemoryType.STRATEGIC and tags and not keywords and not key_pattern:
                # Fast path: use index for tag-based searches
                matching_keys = self.strategic_index.find_by_tags(tags, match_all=False)
                memories = []
                for key in matching_keys:
                    memory = await self.get(key)
                    if memory:
                        memories.append(memory)
                
                # Apply pagination
                return memories[offset:offset + limit]
            
            # Standard search path
            # Get all memories to search from
            if memory_type:
                all_memories = await self.list(memory_type)
            else:
                # Get all memories from all types
                all_memories = []
                for mem_type in MemoryType:
                    all_memories.extend(await self.list(mem_type))
            
            # Apply filters
            filtered_memories = all_memories
            
            # Filter by key pattern
            if key_pattern:
                filtered_memories = [
                    m for m in filtered_memories 
                    if key_pattern.lower() in m.key.lower()
                ]
            
            # Filter by keywords in content
            if keywords:
                def matches_keywords(memory: Memory) -> bool:
                    content_str = json.dumps(memory.content).lower()
                    return any(keyword.lower() in content_str for keyword in keywords)
                
                filtered_memories = [
                    m for m in filtered_memories
                    if matches_keywords(m)
                ]
            
            # Filter by tags
            if tags:
                filtered_memories = [
                    m for m in filtered_memories
                    if any(tag in m.get_tags() for tag in tags)
                ]
            
            # Apply pagination
            paginated_memories = filtered_memories[offset:offset + limit]
            
            return paginated_memories
            
        except Exception as e:
            raise RepositoryError(f"Failed to search memories: {e}")
    
    async def get_by_version(self, key: str, version: int) -> Optional[Memory]:
        """Retrieve a specific version of a memory.
        
        For file-based storage, we store version history in a subdirectory.
        
        Args:
            key: Memory key
            version: Version number to retrieve
            
        Returns:
            Memory instance if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        try:
            # Try to find the versioned memory file
            for memory_type in MemoryType:
                dir_name = self._get_directory_name(memory_type)
                safe_key = key.replace("/", "_").replace("\\", "_")
                version_file = f"{dir_name}/.versions/{safe_key}_v{version}.json"
                
                if self.storage.exists(version_file):
                    data = self.storage.load(version_file)
                    return self._dict_to_memory(data)
            
            return None
            
        except Exception as e:
            raise RepositoryError(f"Failed to get memory version: {e}")
    
    async def list_versions(self, key: str) -> List[int]:
        """List all available versions of a memory.
        
        Args:
            key: Memory key
            
        Returns:
            List of version numbers
            
        Raises:
            RepositoryError: If list operation fails
        """
        try:
            versions = []
            safe_key = key.replace("/", "_").replace("\\", "_")
            
            for memory_type in MemoryType:
                dir_name = self._get_directory_name(memory_type)
                version_dir = self.storage.get_full_path(f"{dir_name}/.versions")
                
                if not version_dir.exists():
                    continue
                
                # Find all version files for this key
                for file_path in version_dir.glob(f"{safe_key}_v*.json"):
                    # Extract version number from filename
                    filename = file_path.stem  # e.g., "mykey_v1"
                    version_str = filename.split('_v')[-1]
                    try:
                        version_num = int(version_str)
                        versions.append(version_num)
                    except ValueError:
                        continue
            
            return sorted(versions)
            
        except Exception as e:
            raise RepositoryError(f"Failed to list memory versions: {e}")
    
    async def _save_version(self, memory: Memory) -> None:
        """Save a versioned copy of the memory.
        
        Args:
            memory: Memory to save version of
        """
        import logging
        
        try:
            version = memory.get_version()
            dir_name = self._get_directory_name(memory.type)
            safe_key = memory.key.replace("/", "_").replace("\\", "_")
            
            # Ensure version directory exists
            version_dir = f"{dir_name}/.versions"
            self.storage.ensure_directory(version_dir)
            
            # Save versioned copy
            version_file = f"{version_dir}/{safe_key}_v{version}.json"
            data = self._memory_to_dict(memory)
            self.storage.save(version_file, data)
            
        except Exception as e:
            # Log error but don't fail the save operation
            logging.warning(f"Failed to save memory version: {e}")
    
    def _update_strategic_index(self, memory: Memory) -> None:
        """Update the strategic memory index for a memory.
        
        Args:
            memory: Memory to index
        """
        # Determine entry type
        entry_type = None
        if memory.has_tag("adr"):
            entry_type = "adr"
        elif memory.has_tag("goal") or "goal" in memory.content:
            entry_type = "goal"
        
        # Get priority and status from content
        priority = memory.content.get("priority")
        status = memory.content.get("status")
        tags = memory.get_tags()
        
        # Add to index
        if entry_type:
            self.strategic_index.add_entry(
                key=memory.key,
                entry_type=entry_type,
                priority=priority,
                status=status,
                tags=tags
            )
