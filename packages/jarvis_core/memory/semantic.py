"""Semantic memory module for embedding storage and retrieval.

This module provides an interface for storing and retrieving semantic embeddings,
which represent knowledge in a vector space. It is designed to integrate with
pgvector for efficient similarity search in the future.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

from jarvis_core.shared.exceptions import RepositoryError


class SemanticMemoryInterface(ABC):
    """Abstract interface for semantic memory operations.
    
    This interface defines the contract for embedding storage and retrieval.
    Implementations can use various vector databases (e.g., pgvector, FAISS,
    Pinecone) for efficient similarity search.
    
    Future implementation will integrate with pgvector for Postgres-based
    vector storage and similarity search.
    """
    
    @abstractmethod
    def store_embedding(
        self,
        key: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Store an embedding vector with associated metadata.
        
        Args:
            key: Unique identifier for the embedding
            embedding: Vector representation (list of floats)
            metadata: Optional metadata to store with the embedding
            
        Raises:
            RepositoryError: If storage operation fails
            ValueError: If embedding is invalid
        """
        pass
    
    @abstractmethod
    def retrieve_embedding(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve an embedding by its key.
        
        Args:
            key: Unique identifier for the embedding
            
        Returns:
            Dictionary containing embedding and metadata, or None if not found
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        pass
    
    @abstractmethod
    def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar embeddings using vector similarity.
        
        Args:
            query_embedding: Query vector to search for
            top_k: Number of top results to return
            threshold: Optional similarity threshold (0-1)
            
        Returns:
            List of dictionaries containing matching embeddings with similarity scores
            
        Raises:
            RepositoryError: If search operation fails
            ValueError: If query_embedding is invalid
        """
        pass
    
    @abstractmethod
    def delete_embedding(self, key: str) -> bool:
        """Delete an embedding by its key.
        
        Args:
            key: Unique identifier for the embedding to delete
            
        Returns:
            True if deletion was successful, False if key not found
            
        Raises:
            RepositoryError: If deletion operation fails
        """
        pass
    
    @abstractmethod
    def list_embeddings(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List stored embeddings with pagination.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List of dictionaries containing embedding metadata
            
        Raises:
            RepositoryError: If list operation fails
        """
        pass


class InMemorySemanticStore(SemanticMemoryInterface):
    """In-memory implementation of semantic memory store.
    
    This is a simple implementation for development and testing. It stores
    embeddings in memory and uses basic cosine similarity for search.
    
    For production use, this should be replaced with a pgvector-based
    implementation for efficient and persistent vector storage.
    """
    
    def __init__(self):
        """Initialize in-memory semantic store."""
        self._embeddings: Dict[str, Dict[str, Any]] = {}
    
    def store_embedding(
        self,
        key: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Store an embedding vector with associated metadata.
        
        Args:
            key: Unique identifier for the embedding
            embedding: Vector representation (list of floats)
            metadata: Optional metadata to store with the embedding
            
        Raises:
            ValueError: If key is empty or embedding is invalid
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        if not isinstance(embedding, list) or not embedding:
            raise ValueError("Embedding must be a non-empty list")
        
        if not all(isinstance(x, (int, float)) for x in embedding):
            raise ValueError("Embedding must contain only numeric values")
        
        self._embeddings[key] = {
            "embedding": embedding,
            "metadata": metadata or {},
            "key": key
        }
    
    def retrieve_embedding(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve an embedding by its key.
        
        Args:
            key: Unique identifier for the embedding
            
        Returns:
            Dictionary containing embedding and metadata, or None if not found
        """
        return self._embeddings.get(key)
    
    def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar embeddings using cosine similarity.
        
        Args:
            query_embedding: Query vector to search for
            top_k: Number of top results to return
            threshold: Optional similarity threshold (0-1)
            
        Returns:
            List of dictionaries containing matching embeddings with similarity scores
            
        Raises:
            ValueError: If query_embedding is invalid or top_k is not positive
        """
        if not isinstance(query_embedding, list) or not query_embedding:
            raise ValueError("Query embedding must be a non-empty list")
        
        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        
        if threshold is not None and (threshold < 0 or threshold > 1):
            raise ValueError("Threshold must be between 0 and 1")
        
        results = []
        
        for key, data in self._embeddings.items():
            similarity = self._cosine_similarity(query_embedding, data["embedding"])
            
            if threshold is None or similarity >= threshold:
                results.append({
                    "key": key,
                    "embedding": data["embedding"],
                    "metadata": data["metadata"],
                    "similarity": similarity
                })
        
        # Sort by similarity (descending) and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def delete_embedding(self, key: str) -> bool:
        """Delete an embedding by its key.
        
        Args:
            key: Unique identifier for the embedding to delete
            
        Returns:
            True if deletion was successful, False if key not found
        """
        if key in self._embeddings:
            del self._embeddings[key]
            return True
        return False
    
    def list_embeddings(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List stored embeddings with pagination.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List of dictionaries containing embedding metadata
            
        Raises:
            ValueError: If limit or offset is negative
        """
        if limit < 0 or offset < 0:
            raise ValueError("Limit and offset must be non-negative")
        
        keys = list(self._embeddings.keys())
        paginated_keys = keys[offset:offset + limit]
        
        return [
            {
                "key": key,
                "metadata": self._embeddings[key]["metadata"],
                "dimension": len(self._embeddings[key]["embedding"])
            }
            for key in paginated_keys
        ]
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# Module-level store instance (singleton pattern)
_store: Optional[InMemorySemanticStore] = None


def get_semantic_store() -> SemanticMemoryInterface:
    """Get the semantic memory store instance.
    
    Returns:
        SemanticMemoryInterface implementation
        
    Note:
        Currently returns an in-memory implementation. In production,
        this should be configured to return a pgvector-based implementation.
    """
    global _store
    if _store is None:
        _store = InMemorySemanticStore()
    return _store
