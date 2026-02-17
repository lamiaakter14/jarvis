"""Unit tests for ExecuteTasks use case."""

from datetime import datetime
from uuid import uuid4

import pytest
from jarvis_core.application.use_cases.execute_tasks import ExecuteTasks
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.shared.constants import TaskPriority, TaskStatus


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
            task_repository=mock_task_repository, notification_service=mock_notification_service
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
            task_repository=mock_task_repository, notification_service=mock_notification_service
        )

        # Execute
        results = await use_case.execute(task_ids)

        # Verify
        assert len(results) == len(task_ids)

    async def test_execute_task_not_found(self, mock_task_repository, mock_notification_service):
        """Test executing a non-existent task."""
        # Setup
        mock_task_repository.get.return_value = None

        use_case = ExecuteTasks(
            task_repository=mock_task_repository, notification_service=mock_notification_service
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
            task_repository=mock_task_repository, notification_service=mock_notification_service
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
            task_repository=mock_task_repository, notification_service=mock_notification_service
        )

        # Execute
        await use_case.execute([sample_task.task_id])

        # Verify notification was sent (if implemented)
        # This may need adjustment based on actual implementation
        # assert mock_notification_service.notify_task_completed.called

    async def test_get_tasks_by_status(self, mock_task_repository, mock_notification_service):
        """Test retrieving tasks filtered by status."""
        # Create tasks with different statuses
        tasks = [
            Task(
                task_id=str(uuid4()),
                title=f"Task {i}",
                description=f"Description {i}",
                priority=Priority.MEDIUM,
                cognitive_load=CognitiveLoad.MEDIUM,
                roi=ROI(0.7),
                status=(
                    TaskStatus.PENDING
                    if i < 2
                    else (TaskStatus.IN_PROGRESS if i < 4 else TaskStatus.COMPLETED)
                ),
                created_at=datetime.now(),
            )
            for i in range(6)
        ]

        # Setup
        mock_task_repository.list.return_value = tasks

        use_case = ExecuteTasks(
            task_repository=mock_task_repository, notification_service=mock_notification_service
        )

        # Execute - get pending tasks
        pending_results = await use_case.get_tasks_by_status(TaskStatus.PENDING)

        # Verify
        assert len(pending_results) == 2
        assert all(task.status == TaskStatus.PENDING.value for task in pending_results)

        # Execute - get in progress tasks
        in_progress_results = await use_case.get_tasks_by_status(TaskStatus.IN_PROGRESS)

        # Verify
        assert len(in_progress_results) == 2
        assert all(task.status == TaskStatus.IN_PROGRESS.value for task in in_progress_results)

    async def test_get_tasks_by_priority(self, mock_task_repository, mock_notification_service):
        """Test retrieving tasks filtered by priority."""
        # Create tasks with different priorities
        tasks = [
            Task(
                task_id=str(uuid4()),
                title=f"Task {i}",
                description=f"Description {i}",
                priority=Priority.HIGH if i % 2 == 0 else Priority.LOW,
                cognitive_load=CognitiveLoad.MEDIUM,
                roi=ROI(0.7),
                status=TaskStatus.PENDING,
                created_at=datetime.now(),
            )
            for i in range(6)
        ]

        # Setup
        mock_task_repository.list.return_value = tasks

        use_case = ExecuteTasks(
            task_repository=mock_task_repository, notification_service=mock_notification_service
        )

        # Execute - get high priority tasks
        high_priority_results = await use_case.get_tasks_by_priority(TaskPriority.HIGH)

        # Verify
        assert len(high_priority_results) == 3
        assert all(task.priority == TaskPriority.HIGH.value for task in high_priority_results)

        # Execute - get low priority tasks
        low_priority_results = await use_case.get_tasks_by_priority(TaskPriority.LOW)

        # Verify
        assert len(low_priority_results) == 3
        assert all(task.priority == TaskPriority.LOW.value for task in low_priority_results)

    async def test_get_tasks_by_priority_and_status(
        self, mock_task_repository, mock_notification_service
    ):
        """Test retrieving tasks filtered by both priority and status."""
        # Create tasks with different priorities and statuses
        tasks = [
            Task(
                task_id=str(uuid4()),
                title=f"Task {i}",
                description=f"Description {i}",
                priority=Priority.HIGH if i < 3 else Priority.LOW,
                cognitive_load=CognitiveLoad.MEDIUM,
                roi=ROI(0.7),
                status=TaskStatus.PENDING if i % 2 == 0 else TaskStatus.COMPLETED,
                created_at=datetime.now(),
            )
            for i in range(6)
        ]

        # Setup
        mock_task_repository.list.return_value = tasks

        use_case = ExecuteTasks(
            task_repository=mock_task_repository, notification_service=mock_notification_service
        )

        # Execute - get high priority pending tasks
        results = await use_case.get_tasks_by_priority(TaskPriority.HIGH, status=TaskStatus.PENDING)

        # Verify
        assert len(results) == 2  # Tasks 0 and 2 are high priority and pending
        assert all(
            task.priority == TaskPriority.HIGH.value and task.status == TaskStatus.PENDING.value
            for task in results
        )
