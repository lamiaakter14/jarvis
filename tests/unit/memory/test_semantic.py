"""Unit tests for semantic memory module."""

import pytest

from jarvis_core.memory.semantic import (
    SemanticMemoryInterface,
    InMemorySemanticStore,
    get_semantic_store
)


@pytest.mark.unit
class TestInMemorySemanticStore:
    """Test in-memory semantic store functionality."""
    
    @pytest.fixture
    def store(self):
        """Create an in-memory semantic store for testing."""
        return InMemorySemanticStore()
    
    def test_store_initialization(self, store):
        """Test that store initializes correctly."""
        assert store is not None
        assert store._embeddings == {}
    
    def test_store_embedding(self, store):
        """Test storing an embedding."""
        key = "test_key"
        embedding = [0.1, 0.2, 0.3, 0.4]
        metadata = {"source": "test"}
        
        store.store_embedding(key, embedding, metadata)
        
        result = store.retrieve_embedding(key)
        assert result is not None
        assert result["embedding"] == embedding
        assert result["metadata"] == metadata
        assert result["key"] == key
    
    def test_store_embedding_without_metadata(self, store):
        """Test storing an embedding without metadata."""
        key = "test_key"
        embedding = [0.1, 0.2, 0.3]
        
        store.store_embedding(key, embedding)
        
        result = store.retrieve_embedding(key)
        assert result is not None
        assert result["embedding"] == embedding
        assert result["metadata"] == {}
    
    def test_store_empty_key_raises_error(self, store):
        """Test that empty key raises ValueError."""
        with pytest.raises(ValueError, match="Key cannot be empty"):
            store.store_embedding("", [0.1, 0.2])
    
    def test_store_invalid_embedding_raises_error(self, store):
        """Test that invalid embeddings raise ValueError."""
        with pytest.raises(ValueError, match="must be a non-empty list"):
            store.store_embedding("key", [])
        
        with pytest.raises(ValueError, match="must be a non-empty list"):
            store.store_embedding("key", "not a list")
        
        with pytest.raises(ValueError, match="must contain only numeric values"):
            store.store_embedding("key", [0.1, "invalid", 0.3])
    
    def test_retrieve_nonexistent_embedding(self, store):
        """Test retrieving a non-existent embedding returns None."""
        result = store.retrieve_embedding("nonexistent")
        assert result is None
    
    def test_delete_embedding(self, store):
        """Test deleting an embedding."""
        key = "test_key"
        store.store_embedding(key, [0.1, 0.2, 0.3])
        
        assert store.delete_embedding(key) is True
        assert store.retrieve_embedding(key) is None
    
    def test_delete_nonexistent_embedding(self, store):
        """Test deleting a non-existent embedding returns False."""
        assert store.delete_embedding("nonexistent") is False
    
    def test_search_similar(self, store):
        """Test searching for similar embeddings."""
        # Store some embeddings
        store.store_embedding("emb1", [1.0, 0.0, 0.0], {"label": "A"})
        store.store_embedding("emb2", [0.9, 0.1, 0.0], {"label": "B"})
        store.store_embedding("emb3", [0.0, 1.0, 0.0], {"label": "C"})
        
        # Search for similar to [1.0, 0.0, 0.0]
        results = store.search_similar([1.0, 0.0, 0.0], top_k=2)
        
        assert len(results) == 2
        assert results[0]["key"] == "emb1"  # Exact match should be first
        assert results[1]["key"] == "emb2"  # Close match should be second
        assert results[0]["similarity"] > results[1]["similarity"]
    
    def test_search_similar_with_threshold(self, store):
        """Test searching with similarity threshold."""
        store.store_embedding("emb1", [1.0, 0.0, 0.0])
        store.store_embedding("emb2", [0.5, 0.5, 0.0])
        store.store_embedding("emb3", [0.0, 1.0, 0.0])
        
        # Search with high threshold
        results = store.search_similar([1.0, 0.0, 0.0], top_k=10, threshold=0.9)
        
        # Only very similar embeddings should be returned
        assert len(results) <= 2
        assert all(r["similarity"] >= 0.9 for r in results)
    
    def test_search_invalid_query_raises_error(self, store):
        """Test that invalid query raises ValueError."""
        with pytest.raises(ValueError, match="must be a non-empty list"):
            store.search_similar([], top_k=5)
        
        with pytest.raises(ValueError, match="must be a positive integer"):
            store.search_similar([0.1, 0.2], top_k=0)
        
        with pytest.raises(ValueError, match="must be a positive integer"):
            store.search_similar([0.1, 0.2], top_k=-1)
        
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            store.search_similar([0.1, 0.2], threshold=1.5)
    
    def test_list_embeddings(self, store):
        """Test listing embeddings."""
        store.store_embedding("emb1", [0.1, 0.2], {"type": "A"})
        store.store_embedding("emb2", [0.3, 0.4], {"type": "B"})
        store.store_embedding("emb3", [0.5, 0.6], {"type": "C"})
        
        results = store.list_embeddings()
        
        assert len(results) == 3
        assert all("key" in r for r in results)
        assert all("metadata" in r for r in results)
        assert all("dimension" in r for r in results)
    
    def test_list_embeddings_with_pagination(self, store):
        """Test listing embeddings with pagination."""
        for i in range(10):
            store.store_embedding(f"emb{i}", [float(i), 0.0])
        
        # Get first page
        page1 = store.list_embeddings(limit=3, offset=0)
        assert len(page1) == 3
        
        # Get second page
        page2 = store.list_embeddings(limit=3, offset=3)
        assert len(page2) == 3
        
        # Ensure pages are different
        keys_page1 = {r["key"] for r in page1}
        keys_page2 = {r["key"] for r in page2}
        assert keys_page1.isdisjoint(keys_page2)
    
    def test_list_embeddings_invalid_params_raises_error(self, store):
        """Test that invalid pagination params raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            store.list_embeddings(limit=-1)
        
        with pytest.raises(ValueError, match="must be non-negative"):
            store.list_embeddings(offset=-1)
    
    def test_cosine_similarity_calculation(self):
        """Test cosine similarity calculation."""
        # Test identical vectors
        similarity = InMemorySemanticStore._cosine_similarity([1.0, 0.0], [1.0, 0.0])
        assert abs(similarity - 1.0) < 0.001
        
        # Test orthogonal vectors
        similarity = InMemorySemanticStore._cosine_similarity([1.0, 0.0], [0.0, 1.0])
        assert abs(similarity - 0.0) < 0.001
        
        # Test opposite vectors
        similarity = InMemorySemanticStore._cosine_similarity([1.0, 0.0], [-1.0, 0.0])
        assert abs(similarity - (-1.0)) < 0.001
        
        # Test different length vectors
        similarity = InMemorySemanticStore._cosine_similarity([1.0, 0.0], [1.0, 0.0, 0.0])
        assert similarity == 0.0


@pytest.mark.unit
class TestSemanticModuleFunctions:
    """Test module-level functions."""
    
    def test_get_semantic_store(self):
        """Test get_semantic_store function."""
        store1 = get_semantic_store()
        store2 = get_semantic_store()
        
        # Should return singleton instance
        assert store1 is store2
        assert isinstance(store1, SemanticMemoryInterface)
