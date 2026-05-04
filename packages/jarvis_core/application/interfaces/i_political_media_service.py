"""Interface for the Political Media OS content generation service."""

from abc import ABC, abstractmethod
from typing import Any

from jarvis_core.domain.entities.political_media import (
    PoliticalKnowledgeContext,
    PoliticalMediaCommand,
    PoliticalMediaResult,
)


class IPoliticalMediaService(ABC):
    """Abstract interface for political media content generation.

    Defines the contract for all generation modules used by the
    PoliticalMediaAgent (Mahedi Engine v1).
    """

    @abstractmethod
    async def generate_facebook_post(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a Facebook post for the given topic and context.

        Args:
            command: Parsed user command with topic and optional parameters.
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with the generated post.
        """

    @abstractmethod
    async def generate_comment_reply(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a reply to a social-media comment.

        Args:
            command: Parsed command where *topic* is the original comment text
                and *context* may contain additional framing.
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with the generated reply.
        """

    @abstractmethod
    async def generate_reel_script(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a short-form video (reel) script.

        Args:
            command: Parsed command with topic and optional duration hint in
                *context* (e.g. "30s", "60s").
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with scene-by-scene reel script.
        """

    @abstractmethod
    async def generate_blog_content(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate long-form website or blog article content.

        Args:
            command: Parsed command with topic and optional SEO keywords in
                *context*.
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with full article text and SEO metadata.
        """

    @abstractmethod
    async def fix_blogger_xml(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Detect and fix errors in a Blogger XML template.

        Args:
            command: Parsed command where *context* contains the raw XML
                string to repair.
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with corrected XML and a summary of fixes.
        """

    @abstractmethod
    async def generate_political_strategy(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a political strategy briefing for a given situation.

        Args:
            command: Parsed command with the strategic situation in *topic*
                and optional constraints in *context*.
            knowledge: Reusable political knowledge and brand context.

        Returns:
            PoliticalMediaResult with a structured strategy document.
        """

    @abstractmethod
    def apply_qa(
        self,
        result: PoliticalMediaResult,
        command: PoliticalMediaCommand,
    ) -> PoliticalMediaResult:
        """Apply consistency, safety, and formatting checks to a result.

        Args:
            result: Raw generated result to validate.
            command: Original command for context.

        Returns:
            Result with qa_flags populated (content unchanged).
        """

    @abstractmethod
    def package_output(
        self,
        result: PoliticalMediaResult,
        command: PoliticalMediaCommand,
    ) -> dict[str, Any]:
        """Package the result into a platform-ready output dictionary.

        Args:
            result: Validated PoliticalMediaResult.
            command: Original command for context.

        Returns:
            Dictionary ready for API or CLI presentation.
        """
