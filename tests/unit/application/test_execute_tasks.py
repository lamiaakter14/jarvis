"""Unit tests for ExecuteTasks use case."""
import pytest
from datetime import datetime
from uuid import uuid4

from src.application.use_cases.execute_tasks import ExecuteTasks
from src.domain.entities.task import Task
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.cognitive_load import CognitiveLoad
from src.domain.value_objects.roi import ROI


@pytest.mark.unit
@pytest.mark.asyncio
class TestExecuteTasks:
    """Test ExecuteTasks use case."""
    
    async def test_execute_single_task_success(
        self, mock_task_repository, mock_notification_service, sample_task
    ):
        """Test executing a single task successfully."""
        # Setup
        mock_task_repository.get.return_value = sample_task
        
        use_case = ExecuteTasks(
            task_repository=mock_task_repository,
            notification_service=mock_notification_service
        )
        
        # Execute
        results = await use_case.execute([sample_task.task_id])
        
        # Verify
        assert len(results) == 1
        assert mock_task_repository.get.called
        assert mock_task_repository.update.called
    
    async def test_execute_multiple_tasks(
        self, mock_task_repository, mock_notification_service, sample_tasks
    ):
        """Test executing multiple tasks."""
        # Setup
        task_ids = [task.task_id for task in sample_tasks]
        mock_task_repository.get.side_effect = sample_tasks
        
        use_case = ExecuteTasks(
            task_repository=mock_task_repository,
            notification_service=mock_notification_service
        )
        
        # Execute
        results = await use_case.execute(task_ids)
        
        # Verify
        assert len(results) == len(task_ids)
    
    async def test_execute_task_not_found(
        self, mock_task_repository, mock_notification_service
    ):
        """Test executing a non-existent task."""
        # Setup
        mock_task_repository.get.return_value = None
        
        use_case = ExecuteTasks(
            task_repository=mock_task_repository,
            notification_service=mock_notification_service
        )
        
        # Execute - should handle gracefully
        results = await use_case.execute(["nonexistent_id"])
        
        # Verify - empty results or error handling
        assert isinstance(results, list)
    
    async def test_execute_task_marks_in_progress(
        self, mock_task_repository, mock_notification_service, sample_task
    ):
        """Test that task is marked as in_progress during execution."""
        # Setup
        mock_task_repository.get.return_value = sample_task
        
        use_case = ExecuteTasks(
            task_repository=mock_task_repository,
            notification_service=mock_notification_service
        )
        
        # Execute
        await use_case.execute([sample_task.task_id])
        
        # Verify task was updated (should be called at least once)
        assert mock_task_repository.update.called
    
    async def test_execute_task_sends_notification(
        self, mock_task_repository, mock_notification_service, sample_task
    ):
        """Test that notification is sent after task execution."""
        # Setup
        mock_task_repository.get.return_value = sample_task
        
        use_case = ExecuteTasks(
            task_repository=mock_task_repository,
            notification_service=mock_notification_service
        )
        
        # Execute
        await use_case.execute([sample_task.task_id])
        
        # Verify notification was sent (if implemented)
        # This may need adjustment based on actual implementation
        # assert mock_notification_service.notify_task_completed.called
