"""Memory Data Transfer Object for application layer."""

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType


class MemoryDTO(BaseModel):
    """Data Transfer Object for Memory entity.
    
    Provides a serializable representation of memories for API and
    application layer communication with comprehensive data validation.
    """
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    memory_id: str = Field(..., description="Unique identifier for the memory")
    type: str = Field(..., description="Type of memory (working, knowledge, strategic, execution_log)")
    key: str = Field(..., min_length=1, description="Unique key identifying the memory")
    content: Dict[str, Any] = Field(..., description="Memory content as dictionary")
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    version: int = Field(default=1, ge=1, description="Memory version number")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate memory type is valid."""
        try:
            MemoryType(v)
            return v
        except ValueError:
            valid_types = [t.value for t in MemoryType]
            raise ValueError(f"Invalid memory type '{v}'. Must be one of: {valid_types}")
    
    @field_validator('key')
    @classmethod
    def validate_key(cls, v: str) -> str:
        """Validate memory key is not empty."""
        if not v or not v.strip():
            raise ValueError("Memory key cannot be empty")
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate memory content is a dictionary."""
        if not isinstance(v, dict):
            raise ValueError("Memory content must be a dictionary")
        return v
    
    @classmethod
    def from_entity(cls, memory: Memory) -> "MemoryDTO":
        """Convert Memory entity to DTO.
        
        Args:
            memory: Memory entity to convert
            
        Returns:
            MemoryDTO instance
        """
        return cls(
            memory_id=memory.memory_id,
            type=memory.type.value,
            key=memory.key,
            content=memory.content,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
            metadata=memory.metadata,
            version=memory.metadata.get('version', 1),
        )
    
    def to_entity(self) -> Memory:
        """Convert DTO to Memory entity.
        
        Returns:
            Memory entity instance
        """
        # Create memory with validated data
        memory = Memory(
            memory_id=self.memory_id,
            type=MemoryType(self.type),
            key=self.key,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
            metadata=self.metadata,
        )
        
        # Store version in metadata
        memory.metadata['version'] = self.version
        
        return memory
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary.
        
        Returns:
            Dictionary representation of the memory
        """
        return self.model_dump()


class MemorySearchQueryDTO(BaseModel):
    """DTO for memory search queries."""
    
    model_config = ConfigDict(use_enum_values=True)
    
    memory_type: Optional[str] = Field(None, description="Filter by memory type")
    keywords: Optional[list[str]] = Field(None, description="Keywords to search for")
    key_pattern: Optional[str] = Field(None, description="Pattern to match in keys")
    context: Optional[Dict[str, Any]] = Field(None, description="Context for semantic search")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum results to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    
    @field_validator('memory_type')
    @classmethod
    def validate_memory_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate memory type if provided."""
        if v is not None:
            try:
                MemoryType(v)
            except ValueError:
                valid_types = [t.value for t in MemoryType]
                raise ValueError(f"Invalid memory type '{v}'. Must be one of: {valid_types}")
        return v


class MemorySearchResultDTO(BaseModel):
    """DTO for memory search results."""
    
    model_config = ConfigDict(from_attributes=True)
    
    memories: list[MemoryDTO] = Field(default_factory=list, description="List of matching memories")
    total_count: int = Field(..., ge=0, description="Total number of matching memories")
    offset: int = Field(..., ge=0, description="Current offset")
    limit: int = Field(..., ge=1, description="Results limit")
    has_more: bool = Field(..., description="Whether more results are available")
