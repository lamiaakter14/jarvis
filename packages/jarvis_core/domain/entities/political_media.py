"""Domain entities for Political Media OS – Mahedi Engine v1.

Defines the command, context, and result models used by the
PoliticalMediaAgent to generate political media content and strategy.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from jarvis_core.shared.utils import generate_id


class MediaCommand(str, Enum):
    """Supported command types for the Political Media OS."""

    POST = "/post"
    REPLY = "/reply"
    REEL = "/reel"
    BLOG = "/blog"
    FIXXML = "/fixxml"
    STRATEGY = "/strategy"


@dataclass
class PoliticalMediaCommand:
    """Represents a parsed user command for the Political Media OS.

    Attributes:
        command: The command type (e.g. /post, /reply).
        topic: Main topic or subject for the content request.
        context: Optional extra context, tone hints, or raw XML to fix.
        audience: Target audience segment (e.g. "youth voters", "rural").
        campaign_theme: Active campaign theme or slogan.
        brand_voice: Preferred tone/voice (e.g. "assertive", "empathetic").
        language: Output language (default "Bengali" for Mahedi engine).
        command_id: Unique identifier for this command.
    """

    command: MediaCommand
    topic: str
    context: Optional[str] = None
    audience: Optional[str] = None
    campaign_theme: Optional[str] = None
    brand_voice: Optional[str] = None
    language: str = "Bengali"
    command_id: str = field(default_factory=lambda: generate_id("cmd_"))

    @classmethod
    def from_text(cls, text: str) -> "PoliticalMediaCommand":
        """Parse a raw text command string into a PoliticalMediaCommand.

        Expected format:
            /command topic | context | audience | theme | voice | language

        The pipe-separated extras beyond *topic* are all optional.

        Args:
            text: Raw command string from the user.

        Returns:
            Parsed PoliticalMediaCommand.

        Raises:
            ValueError: If the command keyword is unrecognised or topic is missing.
        """
        text = text.strip()
        parts = [p.strip() for p in text.split("|")]

        # First part must start with a recognised /command keyword
        first = parts[0]
        keyword, _, rest = first.partition(" ")
        keyword = keyword.strip().lower()

        try:
            media_command = MediaCommand(keyword)
        except ValueError:
            valid = ", ".join(c.value for c in MediaCommand)
            raise ValueError(
                f"Unknown command '{keyword}'. Valid commands: {valid}"
            )

        topic = rest.strip()
        if not topic:
            raise ValueError("Topic must not be empty.")

        return cls(
            command=media_command,
            topic=topic,
            context=parts[1] if len(parts) > 1 else None,
            audience=parts[2] if len(parts) > 2 else None,
            campaign_theme=parts[3] if len(parts) > 3 else None,
            brand_voice=parts[4] if len(parts) > 4 else None,
            language=parts[5] if len(parts) > 5 else "Bengali",
        )


@dataclass
class PoliticalMediaResult:
    """Output produced by the PoliticalMediaAgent for a single command.

    Attributes:
        command_id: ID of the originating command.
        command: The command type that produced this result.
        primary_output: Main generated content.
        alternate_output: Optional shorter or alternate version.
        hashtags: Suggested hashtags for social posts.
        cta: Call-to-action suggestion.
        qa_flags: List of QA or safety notes raised during generation.
        metadata: Additional structured data (e.g. XML validation report).
        result_id: Unique identifier for this result.
    """

    command_id: str
    command: MediaCommand
    primary_output: str
    alternate_output: Optional[str] = None
    hashtags: list[str] = field(default_factory=list)
    cta: Optional[str] = None
    qa_flags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    result_id: str = field(default_factory=lambda: generate_id("res_"))

    def to_dict(self) -> dict[str, Any]:
        """Serialise the result to a plain dictionary.

        Returns:
            Dictionary representation of this result.
        """
        return {
            "result_id": self.result_id,
            "command_id": self.command_id,
            "command": self.command.value,
            "primary_output": self.primary_output,
            "alternate_output": self.alternate_output,
            "hashtags": self.hashtags,
            "cta": self.cta,
            "qa_flags": self.qa_flags,
            "metadata": self.metadata,
        }


@dataclass
class PoliticalKnowledgeContext:
    """Reusable knowledge and positioning context for content generation.

    This object travels with each command so that generators can apply
    consistent brand voice and political framing without re-configuration.

    Attributes:
        politician_name: Name of the politician or campaign entity.
        party: Political party name.
        constituency: Target constituency or region.
        key_messages: Core messaging pillars for the campaign.
        opponent_names: Names of political opponents (for reply framing).
        achievements: Recent achievements to highlight.
        brand_voice: Default tone (e.g. "populist", "progressive").
        audience_segments: Known audience groups for targeting.
    """

    politician_name: str = ""
    party: str = ""
    constituency: str = ""
    key_messages: list[str] = field(default_factory=list)
    opponent_names: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)
    brand_voice: str = "assertive and empathetic"
    audience_segments: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a plain dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "politician_name": self.politician_name,
            "party": self.party,
            "constituency": self.constituency,
            "key_messages": self.key_messages,
            "opponent_names": self.opponent_names,
            "achievements": self.achievements,
            "brand_voice": self.brand_voice,
            "audience_segments": self.audience_segments,
        }
