"""Political Media OS – Mahedi Engine v1: Agent.

This agent orchestrates the complete Political Media OS command lifecycle:

  Command Interface → Intent Router → Content Engine → QA → Output Packaging

Supported commands
------------------
/post      – Generate a Facebook post
/reply     – Generate a comment reply
/reel      – Generate a reel/short-video script
/blog      – Generate website/blog content
/fixxml    – Fix Blogger XML template errors
/strategy  – Generate a political strategy briefing
"""

import logging
import time
from typing import Any, Optional

from jarvis_core.application.interfaces.i_political_media_service import (
    IPoliticalMediaService,
)
from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.domain.entities.political_media import (
    MediaCommand,
    PoliticalKnowledgeContext,
    PoliticalMediaCommand,
    PoliticalMediaResult,
)
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException

logger = logging.getLogger(__name__)

# Mapping from MediaCommand enum values to routing handler names
_COMMAND_HANDLER_MAP: dict[MediaCommand, str] = {
    MediaCommand.POST: "_handle_post",
    MediaCommand.REPLY: "_handle_reply",
    MediaCommand.REEL: "_handle_reel",
    MediaCommand.BLOG: "_handle_blog",
    MediaCommand.FIXXML: "_handle_fixxml",
    MediaCommand.STRATEGY: "_handle_strategy",
}


class PoliticalMediaAgent(Agent):
    """Agent implementing the Political Media OS – Mahedi Engine v1.

    Accepts a ``PoliticalMediaCommand`` (or a raw command string) and routes
    execution to the appropriate content-generation module via
    ``IPoliticalMediaService``.  Results are persisted to the memory
    repository so the system accumulates campaign history.

    Args:
        media_service: The content generation service with all six modules.
        memory_repo: Repository for persisting generated content.
        knowledge: Optional baseline political knowledge context; a default
            empty context is used when not provided.
    """

    def __init__(
        self,
        media_service: IPoliticalMediaService,
        memory_repo: IMemoryRepository,
        knowledge: Optional[PoliticalKnowledgeContext] = None,
    ) -> None:
        super().__init__(
            agent_type=AgentType.POLITICAL_MEDIA_OS,
            name="Political Media OS – Mahedi Engine v1",
            description=(
                "Generates political Facebook posts, comment replies, reel scripts, "
                "blog content, fixes Blogger XML, and produces political strategy."
            ),
        )
        self.media_service = media_service
        self.memory_repo = memory_repo
        self.knowledge = knowledge or PoliticalKnowledgeContext()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def execute(self, context: Any) -> dict[str, Any]:
        """Execute the agent with a ``PoliticalMediaCommand`` or raw string.

        This is the primary entry point used by the cognitive loop.  It
        accepts either a ``PoliticalMediaCommand`` instance or a raw command
        string (which is parsed automatically).

        Args:
            context: Either a ``PoliticalMediaCommand`` instance or a raw
                command string such as ``"/post আমাদের উন্নয়ন"``

        Returns:
            Platform-ready output dictionary from ``package_output``.

        Raises:
            DomainException: If routing or generation fails.
        """
        start = time.time()
        try:
            command = self._resolve_command(context)
            result = await self._route(command)
            output = self.media_service.package_output(result, command)
            await self._persist(command, result)
            self.track_execution(success=True, execution_time=time.time() - start)
            return output
        except DomainException:
            self.track_execution(success=False, execution_time=time.time() - start)
            raise
        except Exception as exc:
            self.track_execution(success=False, execution_time=time.time() - start)
            raise DomainException(f"PoliticalMediaAgent execution failed: {exc}") from exc

    async def run_command(
        self,
        command: PoliticalMediaCommand,
        knowledge: Optional[PoliticalKnowledgeContext] = None,
    ) -> dict[str, Any]:
        """Convenience method for direct command execution with optional knowledge override.

        Args:
            command: Fully constructed ``PoliticalMediaCommand``.
            knowledge: Optional knowledge context override for this request only.

        Returns:
            Platform-ready output dictionary.
        """
        effective_knowledge = knowledge or self.knowledge
        start = time.time()
        try:
            result = await self._dispatch(command, effective_knowledge)
            output = self.media_service.package_output(result, command)
            await self._persist(command, result)
            self.track_execution(success=True, execution_time=time.time() - start)
            return output
        except DomainException:
            self.track_execution(success=False, execution_time=time.time() - start)
            raise
        except Exception as exc:
            self.track_execution(success=False, execution_time=time.time() - start)
            raise DomainException(f"PoliticalMediaAgent.run_command failed: {exc}") from exc

    # ------------------------------------------------------------------
    # Command routing (Intent Router)
    # ------------------------------------------------------------------

    async def _route(self, command: PoliticalMediaCommand) -> PoliticalMediaResult:
        """Route a command to the correct generation module.

        Args:
            command: Parsed command to route.

        Returns:
            Generated ``PoliticalMediaResult``.

        Raises:
            DomainException: If the command type has no registered handler.
        """
        return await self._dispatch(command, self.knowledge)

    async def _dispatch(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Dispatch a command to the appropriate handler method.

        Args:
            command: Parsed command.
            knowledge: Active knowledge context.

        Returns:
            Generated ``PoliticalMediaResult``.

        Raises:
            DomainException: If the command type has no registered handler.
        """
        handler_name = _COMMAND_HANDLER_MAP.get(command.command)
        if handler_name is None:
            raise DomainException(
                f"No handler registered for command '{command.command.value}'. "
                f"Supported: {[c.value for c in MediaCommand]}"
            )
        handler = getattr(self, handler_name)
        return await handler(command, knowledge)

    # ------------------------------------------------------------------
    # Module handlers (Content Engine Layer)
    # ------------------------------------------------------------------

    async def _handle_post(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.generate_facebook_post(command, knowledge)

    async def _handle_reply(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.generate_comment_reply(command, knowledge)

    async def _handle_reel(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.generate_reel_script(command, knowledge)

    async def _handle_blog(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.generate_blog_content(command, knowledge)

    async def _handle_fixxml(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.fix_blogger_xml(command, knowledge)

    async def _handle_strategy(
        self, command: PoliticalMediaCommand, knowledge: PoliticalKnowledgeContext
    ) -> PoliticalMediaResult:
        return await self.media_service.generate_political_strategy(command, knowledge)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_command(context: Any) -> PoliticalMediaCommand:
        """Convert *context* to a ``PoliticalMediaCommand`` if necessary.

        Args:
            context: Either a ``PoliticalMediaCommand`` or a raw string.

        Returns:
            Resolved ``PoliticalMediaCommand``.

        Raises:
            DomainException: If *context* cannot be converted.
        """
        if isinstance(context, PoliticalMediaCommand):
            return context
        if isinstance(context, str):
            try:
                return PoliticalMediaCommand.from_text(context)
            except ValueError as exc:
                raise DomainException(str(exc)) from exc
        raise DomainException(
            f"PoliticalMediaAgent expects a PoliticalMediaCommand or str, "
            f"got {type(context).__name__}."
        )

    async def _persist(
        self, command: PoliticalMediaCommand, result: PoliticalMediaResult
    ) -> None:
        """Store the generated result in the memory repository.

        Args:
            command: Original command.
            result: Generated result to persist.
        """
        try:
            memory = Memory(
                type=MemoryType.EXECUTION_LOG,
                key=f"political_media_{result.result_id}",
                content={
                    "command": command.command.value,
                    "topic": command.topic,
                    "language": command.language,
                    "result": result.to_dict(),
                },
                metadata={
                    "agent": "political_media_os",
                    "command_id": command.command_id,
                },
            )
            memory.add_tags(["political_media", command.command.value, command.language])
            await self.memory_repo.save(memory)
        except Exception as exc:
            logger.warning(
                "Failed to persist political media result for command %s (%s): %s",
                command.command.value,
                command.command_id,
                exc,
            )
