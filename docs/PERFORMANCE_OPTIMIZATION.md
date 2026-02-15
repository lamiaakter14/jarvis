# Performance Optimization Guide

## Overview

This document describes the performance optimizations implemented in the JARVIS project, focusing on memory management, caching strategies, and general best practices.

## Memory Caching

### CachedMemoryRepository

The `CachedMemoryRepository` is a wrapper around the base memory repository that adds an LRU (Least Recently Used) caching layer to reduce database access latency.

#### Features

- **LRU Caching**: Automatically evicts least-recently-used entries when cache is full
- **Time-based Invalidation**: Cache entries expire after a configurable TTL (default: 5 minutes)
- **Write-through Strategy**: Writes update both cache and underlying storage
- **Cache Statistics**: Built-in monitoring for cache performance
- **Configurable Size**: Adjust cache size based on memory constraints

#### Performance Target

- **Cached Queries**: <500ms response time
- **Cache Hit Rate**: Target >70% for typical workloads

#### Usage

```python
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
from jarvis_core.infrastructure.persistence.cached_memory_repository import CachedMemoryRepository

# Create base repository
base_repo = FileMemoryRepository(base_path="memory")

# Wrap with caching layer
cached_repo = CachedMemoryRepository(
    repository=base_repo,
    cache_size=128,           # Maximum cached entries
    cache_ttl_seconds=300     # 5-minute TTL
)

# Use as normal repository
memory = await cached_repo.get("my_key")
await cached_repo.save(memory)

# Monitor cache performance
stats = cached_repo.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate']}")
print(f"Total hits: {stats['hits']}, misses: {stats['misses']}")
```

#### Configuration Recommendations

| Workload Type | Cache Size | TTL (seconds) |
|---------------|------------|---------------|
| Development   | 32         | 60            |
| Testing       | 64         | 120           |
| Production (Small) | 128   | 300           |
| Production (Large) | 256   | 600           |

#### Cache Invalidation

The cache is automatically invalidated in these scenarios:

1. **Save Operation**: Invalidates list cache (write-through updates entry cache)
2. **Delete Operation**: Invalidates specific entry and list cache
3. **TTL Expiration**: Entries older than TTL are not returned
4. **Manual Clear**: Use `clear_cache()` to force invalidation

#### Monitoring

Monitor cache performance using the built-in statistics:

```python
stats = cached_repo.get_cache_stats()

# Key metrics
cache_hit_rate = stats['hit_rate']      # Target: >70%
total_requests = stats['hits'] + stats['misses']
eviction_rate = stats['evictions'] / total_requests  # Target: <10%
```

## Security Enhancements

### Filename Sanitization

The improved `sanitize_filename()` function provides comprehensive protection against:

#### Security Features

1. **Path Traversal Protection**
   - Removes `../` and `..\` sequences
   - Strips directory separators (`/`, `\`)
   - Only keeps the filename component

2. **Invalid Character Removal**
   - Removes Windows invalid characters: `< > : " / \ | ? *`
   - Removes control characters (0x00-0x1F)
   - Removes brackets and parentheses for maximum compatibility

3. **Windows Reserved Names**
   - Detects reserved names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
   - Prefixes them with underscore to avoid conflicts

4. **Length Limits**
   - Respects filesystem limits (default: 255 characters)
   - Preserves file extension when truncating

#### Usage

```python
from jarvis_core.shared.utils import sanitize_filename

# Basic usage
safe_name = sanitize_filename("My Document (v2).pdf")
# Result: "My_Document_v2.pdf"

# Path traversal protection
safe_name = sanitize_filename("../../../etc/passwd")
# Result: "passwd"

# Reserved name handling
safe_name = sanitize_filename("CON.txt")
# Result: "_CON.txt"

# Custom max length
safe_name = sanitize_filename("very_long_filename.txt", max_length=50)
```

## Best Practices

### Memory Operations

1. **Use Caching in Production**
   - Always wrap repositories with `CachedMemoryRepository` in production
   - Adjust cache size based on available memory
   - Monitor cache hit rates and adjust TTL accordingly

2. **Batch Operations**
   - Use `list()` operations when fetching multiple memories
   - Avoid individual `get()` calls in loops

3. **Cache Warming**
   - Pre-load frequently accessed memories at startup
   - Use pattern-based queries sparingly (they bypass cache)

### File Operations

1. **Always Sanitize User Input**
   - Use `sanitize_filename()` for any user-provided filenames
   - Validate before and after sanitization
   - Handle errors gracefully

2. **Path Construction**
   - Use `Path` objects for cross-platform compatibility
   - Avoid string concatenation for paths

## Performance Metrics

### Target Metrics

| Operation | Target Latency | Notes |
|-----------|---------------|-------|
| Cached Memory Get | <500ms | 90th percentile |
| Cache Miss Get | <2s | Depends on I/O |
| Memory Save | <1s | Write-through |
| Memory List (Cached) | <500ms | 90th percentile |
| Memory List (Uncached) | <5s | Depends on directory size |

### Monitoring

Track these key performance indicators:

1. **Cache Hit Rate**: >70% is healthy
2. **Average Response Time**: Compare cached vs uncached
3. **Cache Eviction Rate**: <10% is optimal
4. **Memory Usage**: Monitor cache size growth

## Troubleshooting

### Low Cache Hit Rate

- **Cause**: Cache size too small or TTL too short
- **Solution**: Increase `cache_size` or `cache_ttl_seconds`

### High Memory Usage

- **Cause**: Cache size too large
- **Solution**: Reduce `cache_size` or implement cache warming for only hot data

### Stale Data

- **Cause**: TTL too long, external modifications to storage
- **Solution**: Reduce TTL or use manual invalidation

### Performance Degradation

- **Cause**: Cache eviction thrashing
- **Solution**: Increase cache size or optimize access patterns

## Future Enhancements

### Planned Improvements

1. **Distributed Caching**: Redis/Memcached support for multi-instance deployments
2. **Smart Invalidation**: Dependency tracking for intelligent invalidation
3. **Tiered Caching**: L1 (memory) + L2 (Redis) caching strategy
4. **Query Result Caching**: Cache complex search queries
5. **Performance Profiling**: Built-in performance tracing and profiling tools

### Contributing

When adding new features or modifying existing code:

1. Maintain or improve cache hit rates
2. Add tests for cache behavior
3. Document performance characteristics
4. Update this guide with new optimizations
