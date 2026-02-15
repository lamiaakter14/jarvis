"""Memory migration service for handling schema version updates."""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from pydantic import ValidationError

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.schemas.memory_content import validate_memory_content
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.utils import current_timestamp


class MigrationError(Exception):
    """Exception raised when memory migration fails."""
    pass


class MemoryMigration:
    """Handles memory schema migrations and version updates.
    
    Provides tools for:
    - Validating memory content against current schemas
    - Migrating old memory formats to new schemas
    - Handling invalid/incorrect fields gracefully
    - Maintaining backwards compatibility
    """
    
    # Schema version to migration function mapping
    MIGRATIONS: Dict[str, Dict[int, Callable]] = {
        'strategic': {},
        'knowledge': {},
        'working': {},
        'execution_log': {},
        'adr': {}
    }
    
    # Current schema versions for each memory type
    CURRENT_VERSIONS: Dict[str, int] = {
        'strategic': 1,
        'knowledge': 1,
        'working': 1,
        'execution_log': 1,
        'adr': 1
    }
    
    @staticmethod
    def validate_and_fix_memory(memory: Memory) -> tuple[Memory, List[str]]:
        """Validate memory content and attempt to fix invalid fields.
        
        Args:
            memory: Memory instance to validate
            
        Returns:
            Tuple of (fixed_memory, list_of_fixes_applied)
            
        Raises:
            MigrationError: If memory cannot be fixed
        """
        fixes_applied = []
        memory_type_str = memory.type.value if isinstance(memory.type, MemoryType) else str(memory.type)
        
        try:
            # Try to validate with current schema
            validate_memory_content(memory_type_str, memory.content)
            return memory, fixes_applied
        except (ValidationError, ValueError) as e:
            # Validation failed - attempt to fix
            fixes_applied.append(f"Validation failed: {str(e)}")
            
            # Apply fixes based on memory type
            fixed_content = MemoryMigration._apply_fixes(
                memory_type_str,
                memory.content,
                fixes_applied
            )
            
            # Update memory with fixed content
            memory.content = fixed_content
            
            # Validate again
            try:
                validate_memory_content(memory_type_str, memory.content)
                fixes_applied.append("Successfully fixed and validated")
                return memory, fixes_applied
            except (ValidationError, ValueError) as e:
                raise MigrationError(
                    f"Failed to fix memory {memory.key}: {str(e)}"
                )
    
    @staticmethod
    def _apply_fixes(
        memory_type: str,
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Apply type-specific fixes to memory content.
        
        Args:
            memory_type: Type of memory
            content: Memory content to fix
            fixes_log: Log of fixes applied
            
        Returns:
            Fixed content dictionary
        """
        fixed_content = content.copy()
        
        if memory_type == 'strategic':
            fixed_content = MemoryMigration._fix_strategic_memory(
                fixed_content, fixes_log
            )
        elif memory_type == 'adr':
            fixed_content = MemoryMigration._fix_adr_memory(
                fixed_content, fixes_log
            )
        elif memory_type == 'knowledge':
            fixed_content = MemoryMigration._fix_knowledge_memory(
                fixed_content, fixes_log
            )
        elif memory_type == 'execution_log':
            fixed_content = MemoryMigration._fix_execution_log(
                fixed_content, fixes_log
            )
        elif memory_type == 'working':
            fixed_content = MemoryMigration._fix_working_memory(
                fixed_content, fixes_log
            )
        
        return fixed_content
    
    @staticmethod
    def _fix_strategic_memory(
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Fix strategic memory content."""
        fixed = content.copy()
        
        # Ensure required fields
        if 'goal' not in fixed or not fixed['goal']:
            fixed['goal'] = 'Unspecified Goal'
            fixes_log.append("Added default 'goal' field")
        
        # Fix priority field
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if 'priority' not in fixed or fixed['priority'].lower() not in valid_priorities:
            fixed['priority'] = 'medium'
            fixes_log.append("Set default 'priority' to 'medium'")
        else:
            fixed['priority'] = fixed['priority'].lower()
        
        # Fix status field
        valid_statuses = ['active', 'paused', 'completed', 'cancelled']
        if 'status' not in fixed or fixed['status'].lower() not in valid_statuses:
            fixed['status'] = 'active'
            fixes_log.append("Set default 'status' to 'active'")
        else:
            fixed['status'] = fixed['status'].lower()
        
        # Ensure optional fields have correct types
        if 'description' not in fixed:
            fixed['description'] = ''
        if 'progress' not in fixed:
            fixed['progress'] = 0.0
        if 'milestones' not in fixed:
            fixed['milestones'] = []
        if 'dependencies' not in fixed:
            fixed['dependencies'] = []
        if 'metrics' not in fixed:
            fixed['metrics'] = {}
        
        # Validate progress range
        if not 0 <= fixed['progress'] <= 100:
            fixed['progress'] = max(0.0, min(100.0, fixed['progress']))
            fixes_log.append("Clamped 'progress' to valid range [0-100]")
        
        return fixed
    
    @staticmethod
    def _fix_adr_memory(
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Fix ADR memory content."""
        fixed = content.copy()
        
        # Ensure required fields
        if 'title' not in fixed or not fixed['title']:
            fixed['title'] = 'Untitled Decision'
            fixes_log.append("Added default 'title' field")
        
        if 'context' not in fixed or not fixed['context']:
            fixed['context'] = 'No context provided'
            fixes_log.append("Added default 'context' field")
        
        if 'decision' not in fixed or not fixed['decision']:
            fixed['decision'] = 'No decision documented'
            fixes_log.append("Added default 'decision' field")
        
        if 'consequences' not in fixed or not fixed['consequences']:
            fixed['consequences'] = 'No consequences documented'
            fixes_log.append("Added default 'consequences' field")
        
        # Fix status field
        valid_statuses = ['proposed', 'accepted', 'deprecated', 'superseded']
        if 'status' not in fixed or fixed['status'].lower() not in valid_statuses:
            fixed['status'] = 'proposed'
            fixes_log.append("Set default 'status' to 'proposed'")
        else:
            fixed['status'] = fixed['status'].lower()
        
        # Ensure date field
        if 'date' not in fixed:
            fixed['date'] = datetime.now()
            fixes_log.append("Added current date as 'date' field")
        elif isinstance(fixed['date'], str):
            try:
                fixed['date'] = datetime.fromisoformat(fixed['date'].replace('Z', '+00:00'))
            except ValueError:
                fixed['date'] = datetime.now()
                fixes_log.append("Replaced invalid date with current date")
        
        # Ensure optional list fields
        if 'alternatives' not in fixed:
            fixed['alternatives'] = []
        if 'related_decisions' not in fixed:
            fixed['related_decisions'] = []
        
        return fixed
    
    @staticmethod
    def _fix_knowledge_memory(
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Fix knowledge memory content."""
        fixed = content.copy()
        
        # Ensure required fields
        if 'title' not in fixed or not fixed['title']:
            fixed['title'] = 'Untitled Knowledge'
            fixes_log.append("Added default 'title' field")
        
        if 'content' not in fixed or not fixed['content']:
            fixed['content'] = 'No content provided'
            fixes_log.append("Added default 'content' field")
        
        # Ensure optional fields
        if 'description' not in fixed:
            fixed['description'] = ''
        if 'tags' not in fixed:
            fixed['tags'] = []
        if 'confidence' not in fixed:
            fixed['confidence'] = 1.0
        if 'access_count' not in fixed:
            fixed['access_count'] = 0
        
        # Validate confidence range
        if not 0 <= fixed['confidence'] <= 1:
            fixed['confidence'] = max(0.0, min(1.0, fixed['confidence']))
            fixes_log.append("Clamped 'confidence' to valid range [0-1]")
        
        return fixed
    
    @staticmethod
    def _fix_execution_log(
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Fix execution log memory content."""
        fixed = content.copy()
        
        # Ensure required fields
        if 'task_id' not in fixed or not fixed['task_id']:
            fixed['task_id'] = 'unknown'
            fixes_log.append("Added default 'task_id' field")
        
        if 'task_title' not in fixed or not fixed['task_title']:
            fixed['task_title'] = 'Untitled Task'
            fixes_log.append("Added default 'task_title' field")
        
        # Fix status field
        valid_statuses = ['pending', 'in_progress', 'completed', 'failed', 'cancelled']
        if 'status' not in fixed or fixed['status'].lower() not in valid_statuses:
            fixed['status'] = 'completed'
            fixes_log.append("Set default 'status' to 'completed'")
        else:
            fixed['status'] = fixed['status'].lower()
        
        # Ensure started_at field
        if 'started_at' not in fixed:
            fixed['started_at'] = datetime.now()
            fixes_log.append("Added current time as 'started_at' field")
        elif isinstance(fixed['started_at'], str):
            try:
                fixed['started_at'] = datetime.fromisoformat(
                    fixed['started_at'].replace('Z', '+00:00')
                )
            except ValueError:
                fixed['started_at'] = datetime.now()
                fixes_log.append("Replaced invalid started_at with current time")
        
        # Ensure optional fields
        if 'metrics' not in fixed:
            fixed['metrics'] = {}
        
        return fixed
    
    @staticmethod
    def _fix_working_memory(
        content: Dict[str, Any],
        fixes_log: List[str]
    ) -> Dict[str, Any]:
        """Fix working memory content."""
        fixed = content.copy()
        
        # Ensure data field
        if 'data' not in fixed:
            fixed['data'] = {}
            fixes_log.append("Added empty 'data' field")
        
        return fixed
    
    @staticmethod
    async def migrate_memory(
        memory: Memory,
        target_version: Optional[int] = None
    ) -> tuple[Memory, List[str]]:
        """Migrate memory to target schema version.
        
        Args:
            memory: Memory to migrate
            target_version: Target version (defaults to current)
            
        Returns:
            Tuple of (migrated_memory, list_of_migrations_applied)
        """
        migrations_applied = []
        memory_type_str = memory.type.value if isinstance(memory.type, MemoryType) else str(memory.type)
        
        current_version = memory.metadata.get('schema_version', 1)
        if target_version is None:
            target_version = MemoryMigration.CURRENT_VERSIONS.get(memory_type_str, 1)
        
        if current_version == target_version:
            return memory, migrations_applied
        
        # Apply migrations in sequence
        for version in range(current_version + 1, target_version + 1):
            migration_func = MemoryMigration.MIGRATIONS.get(
                memory_type_str, {}
            ).get(version)
            
            if migration_func:
                memory.content = migration_func(memory.content)
                migrations_applied.append(f"Applied migration to version {version}")
        
        # Update schema version in metadata
        memory.metadata['schema_version'] = target_version
        migrations_applied.append(f"Updated schema version to {target_version}")
        
        return memory, migrations_applied
    
    @staticmethod
    async def validate_repository_memories(
        repository: IMemoryRepository,
        memory_type: MemoryType,
        fix_invalid: bool = True
    ) -> Dict[str, Any]:
        """Validate all memories of a given type in repository.
        
        Args:
            repository: Memory repository to validate
            memory_type: Type of memories to validate
            fix_invalid: If True, attempt to fix invalid memories
            
        Returns:
            Validation report with statistics
        """
        report = {
            'total': 0,
            'valid': 0,
            'fixed': 0,
            'failed': 0,
            'errors': []
        }
        
        memories = await repository.list(memory_type)
        report['total'] = len(memories)
        
        for memory in memories:
            try:
                fixed_memory, fixes = MemoryMigration.validate_and_fix_memory(memory)
                
                if fixes:
                    report['fixed'] += 1
                    if fix_invalid:
                        await repository.save(fixed_memory)
                else:
                    report['valid'] += 1
                    
            except MigrationError as e:
                report['failed'] += 1
                report['errors'].append({
                    'key': memory.key,
                    'error': str(e)
                })
        
        return report
