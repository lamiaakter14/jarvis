"""Unit tests for Memory DTO."""

import pytest
from datetime import datetime

from jarvis_core.application.dto.memory_dto import (
    MemoryDTO,
    MemorySearchQueryDTO,
    MemorySearchResultDTO
)
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType


@pytest.mark.unit
class TestMemoryDTO:
    """Test MemoryDTO validation and conversions."""
    
    def test_create_memory_dto(self):
        """Test creating a MemoryDTO with valid data."""
        dto = MemoryDTO(
            memory_id="mem_123",
            type="working",
            key="test_key",
            content={"data": "test"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={},
            version=1
        )
        
        assert dto.memory_id == "mem_123"
        assert dto.type == "working"
        assert dto.key == "test_key"
        assert dto.content == {"data": "test"}
        assert dto.version == 1
    
    def test_memory_dto_validates_type(self):
        """Test that MemoryDTO validates memory type."""
        with pytest.raises(ValueError, match="Invalid memory type"):
            MemoryDTO(
                memory_id="mem_123",
                type="invalid_type",
                key="test_key",
                content={"data": "test"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
    
    def test_memory_dto_validates_key(self):
        """Test that MemoryDTO validates non-empty key."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            MemoryDTO(
                memory_id="mem_123",
                type="working",
                key="",
                content={"data": "test"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
    
    def test_memory_dto_validates_content(self):
        """Test that MemoryDTO validates content is a dictionary."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            MemoryDTO(
                memory_id="mem_123",
                type="working",
                key="test_key",
                content="not a dict",  # type: ignore
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
    
    def test_memory_dto_from_entity(self):
        """Test creating MemoryDTO from Memory entity."""
        memory = Memory(
            memory_id="mem_456",
            type=MemoryType.KNOWLEDGE,
            key="knowledge_key",
            content={"title": "Test Knowledge"},
        )
        
        dto = MemoryDTO.from_entity(memory)
        
        assert dto.memory_id == memory.memory_id
        assert dto.type == memory.type.value
        assert dto.key == memory.key
        assert dto.content == memory.content
    
    def test_memory_dto_to_entity(self):
        """Test converting MemoryDTO to Memory entity."""
        dto = MemoryDTO(
            memory_id="mem_789",
            type="strategic",
            key="strategic_key",
            content={"goal": "Test Goal"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"version": 2},
            version=2
        )
        
        memory = dto.to_entity()
        
        assert memory.memory_id == dto.memory_id
        assert memory.type == MemoryType.STRATEGIC
        assert memory.key == dto.key
        assert memory.content == dto.content
        assert memory.get_version() == 2
    
    def test_memory_dto_to_dict(self):
        """Test converting MemoryDTO to dictionary."""
        dto = MemoryDTO(
            memory_id="mem_123",
            type="working",
            key="test_key",
            content={"data": "test"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        result = dto.to_dict()
        
        assert isinstance(result, dict)
        assert result["memory_id"] == "mem_123"
        assert result["type"] == "working"


@pytest.mark.unit
class TestMemorySearchQueryDTO:
    """Test MemorySearchQueryDTO validation."""
    
    def test_create_search_query(self):
        """Test creating a search query DTO."""
        query = MemorySearchQueryDTO(
            memory_type="knowledge",
            keywords=["test", "search"],
            key_pattern="pattern",
            limit=50,
            offset=10
        )
        
        assert query.memory_type == "knowledge"
        assert query.keywords == ["test", "search"]
        assert query.limit == 50
        assert query.offset == 10
    
    def test_search_query_validates_memory_type(self):
        """Test that search query validates memory type."""
        with pytest.raises(ValueError, match="Invalid memory type"):
            MemorySearchQueryDTO(
                memory_type="invalid_type"
            )
    
    def test_search_query_default_values(self):
        """Test default values in search query."""
        query = MemorySearchQueryDTO()
        
        assert query.memory_type is None
        assert query.keywords is None
        assert query.limit == 100
        assert query.offset == 0
    
    def test_search_query_validates_limit_range(self):
        """Test that limit is within valid range."""
        with pytest.raises(ValueError):
            MemorySearchQueryDTO(limit=0)
        
        with pytest.raises(ValueError):
            MemorySearchQueryDTO(limit=2000)


@pytest.mark.unit
class TestMemorySearchResultDTO:
    """Test MemorySearchResultDTO."""
    
    def test_create_search_result(self):
        """Test creating a search result DTO."""
        memories = [
            MemoryDTO(
                memory_id="mem_1",
                type="working",
                key="key1",
                content={},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        ]
        
        result = MemorySearchResultDTO(
            memories=memories,
            total_count=100,
            offset=0,
            limit=10,
            has_more=True
        )
        
        assert len(result.memories) == 1
        assert result.total_count == 100
        assert result.has_more is True
    
    def test_search_result_empty(self):
        """Test creating an empty search result."""
        result = MemorySearchResultDTO(
            memories=[],
            total_count=0,
            offset=0,
            limit=10,
            has_more=False
        )
        
        assert len(result.memories) == 0
        assert result.total_count == 0
        assert result.has_more is False
