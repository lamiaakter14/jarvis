"""Political Media OS – Mahedi Engine v1: Content Generation Service.

This service implements all six content-generation modules for the
Political Media OS:

  1. Facebook post generation
  2. Comment reply generation
  3. Reel script generation
  4. Website/blog content generation
  5. Blogger XML error fixing
  6. Political strategy generation

Each module builds a specialised prompt, calls the AI backend, and
wraps the response in a PoliticalMediaResult with QA flags and
platform-ready packaging.
"""

import logging
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional

from jarvis_core.application.interfaces.i_political_media_service import (
    IPoliticalMediaService,
)
from jarvis_core.domain.entities.political_media import (
    MediaCommand,
    PoliticalKnowledgeContext,
    PoliticalMediaCommand,
    PoliticalMediaResult,
)
from jarvis_core.shared.exceptions import AIServiceError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety & QA constants
# ---------------------------------------------------------------------------

_MAX_POST_CHARS = 63_206  # Facebook hard limit
_MAX_REPLY_CHARS = 8_000
_REEL_SCENE_MARKER = "SCENE"
_PROHIBITED_PHRASES: list[str] = []  # extend per deployment needs


class PoliticalMediaService(IPoliticalMediaService):
    """Concrete implementation of IPoliticalMediaService.

    Uses an OpenAI-compatible chat-completion backend (injected as
    *ai_client*) with optional mock mode for offline testing.

    Args:
        ai_client: Object with a ``chat_complete(messages, **kwargs)``
            method that returns the assistant reply text.  When *mock_mode*
            is ``True`` the client is never called.
        mock_mode: Return deterministic stub outputs instead of calling the
            AI backend.  Useful for unit tests.
        model: Model identifier forwarded to the AI client.
        temperature: Sampling temperature forwarded to the AI client.
    """

    def __init__(
        self,
        ai_client: Optional[Any] = None,
        mock_mode: bool = False,
        model: str = "gpt-4",
        temperature: float = 0.75,
    ) -> None:
        if not mock_mode and ai_client is None:
            raise AIServiceError(
                "ai_client is required when mock_mode is False."
            )
        self._client = ai_client
        self._mock_mode = mock_mode
        self._model = model
        self._temperature = temperature

    # ------------------------------------------------------------------
    # Public generation methods
    # ------------------------------------------------------------------

    async def generate_facebook_post(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a Facebook post."""
        system = self._system_prompt(knowledge)
        user = (
            f"Write a compelling Facebook post in {command.language} about:\n"
            f"Topic: {command.topic}\n"
            f"{self._optional_fields(command)}"
            "Requirements:\n"
            "- Start with a strong hook\n"
            "- Include relevant emojis\n"
            "- End with a clear call-to-action\n"
            "- Provide a SHORT variant (≤280 chars) and a LONG variant (≤2000 chars)\n"
            "- Suggest 5-8 relevant hashtags\n"
            "Output format:\n"
            "SHORT:\n<short version>\n\nLONG:\n<long version>\n\nHASHTAGS:\n<hashtags>"
        )
        raw = await self._complete(system, user)
        primary, alternate, hashtags = self._parse_post_response(raw)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.POST,
            primary_output=primary,
            alternate_output=alternate,
            hashtags=hashtags,
            cta=self._extract_cta(primary),
        )
        return self.apply_qa(result, command)

    async def generate_comment_reply(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a reply to a social-media comment."""
        system = self._system_prompt(knowledge)
        original_comment = command.topic
        context_note = f"Additional context: {command.context}\n" if command.context else ""
        user = (
            f"Write a professional and persuasive reply in {command.language} to the following "
            f"Facebook comment:\n\n\"{original_comment}\"\n\n"
            f"{context_note}"
            "Requirements:\n"
            "- Acknowledge the commenter respectfully\n"
            "- Address the concern or statement directly\n"
            "- Reinforce the campaign's core message\n"
            "- Keep the reply under 300 words\n"
            "- Optionally include one relevant hashtag\n"
        )
        raw = await self._complete(system, user)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.REPLY,
            primary_output=raw.strip(),
            hashtags=self._extract_hashtags(raw),
        )
        return self.apply_qa(result, command)

    async def generate_reel_script(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a short-form video reel script."""
        system = self._system_prompt(knowledge)
        duration_hint = command.context or "60s"
        user = (
            f"Write a punchy political reel script in {command.language} for a "
            f"{duration_hint} video about:\n"
            f"Topic: {command.topic}\n"
            f"{self._audience_line(command)}"
            "Requirements:\n"
            "- Structure as labelled SCENEs (SCENE 1, SCENE 2 …)\n"
            "- Each scene includes: Visual description | On-screen text | Voiceover\n"
            "- Total script fits within the requested duration\n"
            "- End with a strong call-to-action overlay\n"
            "- Suggest a background music style\n"
        )
        raw = await self._complete(system, user)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.REEL,
            primary_output=raw.strip(),
            metadata={"duration_hint": duration_hint, "scene_count": raw.count(_REEL_SCENE_MARKER)},
        )
        return self.apply_qa(result, command)

    async def generate_blog_content(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate long-form blog/website content."""
        system = self._system_prompt(knowledge)
        seo_hint = command.context or ""
        user = (
            f"Write a detailed, SEO-optimised blog article in {command.language} about:\n"
            f"Topic: {command.topic}\n"
            f"{('SEO keywords: ' + seo_hint + chr(10)) if seo_hint else ''}"
            f"{self._audience_line(command)}"
            "Requirements:\n"
            "- Include an H1 title, introduction, 3-5 H2 sections, and a conclusion\n"
            "- Word count: 800-1200 words\n"
            "- Use factual political context and cite achievements where relevant\n"
            "- End with a call-to-action paragraph\n"
            "- List 5 SEO meta keywords at the end under META_KEYWORDS:\n"
        )
        raw = await self._complete(system, user)
        meta_keywords = self._extract_meta_keywords(raw)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.BLOG,
            primary_output=raw.strip(),
            metadata={"meta_keywords": meta_keywords},
        )
        return self.apply_qa(result, command)

    async def fix_blogger_xml(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Detect and fix errors in a Blogger XML template."""
        raw_xml = command.context or command.topic
        syntax_report = self._validate_xml_syntax(raw_xml)
        errors_found = syntax_report.get("errors", [])

        # Only invoke the AI (or mock) when there are actual errors to fix.
        # When the XML is already valid, return it as-is regardless of mode.
        ai_pass_needed = bool(errors_found)

        if ai_pass_needed:
            system = (
                "You are an expert Blogger (blogspot.com) XML template engineer. "
                "You fix malformed, broken, or non-compliant Blogger XML templates."
            )
            error_list = "\n".join(f"- {e}" for e in errors_found) if errors_found else "none"
            user = (
                "Fix the following Blogger XML template. "
                "Return ONLY the corrected XML without any explanation.\n"
                f"Detected errors:\n{error_list}\n\n"
                f"XML template:\n{raw_xml}"
            )
            corrected_xml = await self._complete(system, user)
            corrected_xml = corrected_xml.strip()
        else:
            corrected_xml = raw_xml

        post_validation = self._validate_xml_syntax(corrected_xml)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.FIXXML,
            primary_output=corrected_xml,
            metadata={
                "original_errors": errors_found,
                "post_fix_valid": post_validation.get("valid", False),
                "post_fix_errors": post_validation.get("errors", []),
                "fixes_applied": len(errors_found),
            },
        )
        if not post_validation.get("valid"):
            result.qa_flags.append(
                "XML still contains structural issues after AI correction. Manual review recommended."
            )
        return result

    async def generate_political_strategy(
        self,
        command: PoliticalMediaCommand,
        knowledge: PoliticalKnowledgeContext,
    ) -> PoliticalMediaResult:
        """Generate a political strategy briefing."""
        system = self._system_prompt(knowledge)
        constraints = command.context or ""
        user = (
            f"Produce a comprehensive political strategy briefing in {command.language} for:\n"
            f"Situation: {command.topic}\n"
            f"{('Constraints: ' + constraints + chr(10)) if constraints else ''}"
            f"{self._audience_line(command)}"
            "Structure:\n"
            "1. SITUATION ANALYSIS – current political landscape\n"
            "2. STRATEGIC OBJECTIVES – 3-5 measurable goals\n"
            "3. KEY MESSAGES – 3 core messages per audience segment\n"
            "4. ACTION PLAN – week-by-week tactical steps\n"
            "5. RISK REGISTER – top 3 risks and mitigations\n"
            "6. MEDIA CALENDAR – suggested content cadence\n"
            "7. SUCCESS METRICS – KPIs to track progress\n"
        )
        raw = await self._complete(system, user)

        result = PoliticalMediaResult(
            command_id=command.command_id,
            command=MediaCommand.STRATEGY,
            primary_output=raw.strip(),
            metadata={"sections": 7},
        )
        return self.apply_qa(result, command)

    # ------------------------------------------------------------------
    # QA & packaging
    # ------------------------------------------------------------------

    def apply_qa(
        self,
        result: PoliticalMediaResult,
        command: PoliticalMediaCommand,
    ) -> PoliticalMediaResult:
        """Run consistency, safety, and length checks on a result.

        Adds warning strings to ``result.qa_flags`` when issues are found.
        The content itself is never modified here.

        Args:
            result: Generated result to inspect.
            command: Original command for context.

        Returns:
            The same result object with ``qa_flags`` updated.
        """
        text = result.primary_output

        # Length checks
        if result.command == MediaCommand.POST and len(text) > _MAX_POST_CHARS:
            result.qa_flags.append(
                f"Post exceeds Facebook's {_MAX_POST_CHARS}-character limit."
            )
        if result.command == MediaCommand.REPLY and len(text) > _MAX_REPLY_CHARS:
            result.qa_flags.append(
                f"Reply exceeds recommended {_MAX_REPLY_CHARS}-character length."
            )

        # Blank output
        if not text.strip():
            result.qa_flags.append("Primary output is empty – generation may have failed.")

        # Prohibited phrase check
        text_lower = text.lower()
        for phrase in _PROHIBITED_PHRASES:
            if phrase.lower() in text_lower:
                result.qa_flags.append(f"Prohibited phrase detected: '{phrase}'")

        # Language consistency hint
        if command.language and command.language.lower() != "english":
            # Heuristic: flag if the output appears to be entirely ASCII (likely English)
            non_ascii_ratio = sum(1 for c in text if ord(c) > 127) / max(len(text), 1)
            if non_ascii_ratio < 0.05 and len(text) > 50:
                result.qa_flags.append(
                    f"Output may not be in the requested language ({command.language}). "
                    "Review before publishing."
                )

        return result

    def package_output(
        self,
        result: PoliticalMediaResult,
        command: PoliticalMediaCommand,
    ) -> dict[str, Any]:
        """Package a validated result into a platform-ready dictionary.

        Args:
            result: Validated PoliticalMediaResult.
            command: Original command for context.

        Returns:
            Dictionary suitable for API response or CLI display.
        """
        output: dict[str, Any] = {
            "engine": "Political Media OS – Mahedi Engine v1",
            "command": command.command.value,
            "topic": command.topic,
            "language": command.language,
        }
        output.update(result.to_dict())

        # Add audience and campaign context when present
        if command.audience:
            output["target_audience"] = command.audience
        if command.campaign_theme:
            output["campaign_theme"] = command.campaign_theme
        if command.brand_voice:
            output["brand_voice"] = command.brand_voice

        if result.qa_flags:
            output["qa_warnings"] = result.qa_flags

        return output

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _complete(self, system: str, user: str) -> str:
        """Send a chat-completion request and return the assistant text.

        In mock mode a deterministic stub is returned so the agent is fully
        testable without a live API key.

        Args:
            system: System prompt text.
            user: User prompt text.

        Returns:
            Assistant reply text.

        Raises:
            AIServiceError: If the AI backend call fails.
        """
        if self._mock_mode:
            return self._mock_response(user)

        try:
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
            return self._client.chat_complete(
                messages=messages,
                model=self._model,
                temperature=self._temperature,
            )
        except Exception as exc:
            raise AIServiceError(f"PoliticalMediaService AI call failed: {exc}") from exc

    @staticmethod
    def _mock_response(user_prompt: str) -> str:
        """Return a deterministic mock response based on prompt keywords."""
        lower = user_prompt.lower()
        if "facebook post" in lower or "post" in lower:
            return (
                "SHORT:\nআমাদের ভবিষ্যৎ, আমাদের পছন্দ! 🇧🇩✊ #পরিবর্তন #উন্নয়ন\n\n"
                "LONG:\nএকটি উন্নত বাংলাদেশের স্বপ্ন নিয়ে আমরা এগিয়ে চলেছি। "
                "আমাদের প্রতিশ্রুতি – শিক্ষা, স্বাস্থ্য ও কর্মসংস্থান। "
                "আপনার ভোট আপনার ভবিষ্যৎ নির্ধারণ করে। সঠিক নেতৃত্ব বেছে নিন।\n\n"
                "HASHTAGS:\n#পরিবর্তন #উন্নয়ন #বাংলাদেশ #ভোট #নেতৃত্ব #রাজনীতি #সংসদ"
            )
        if "reply" in lower or "comment" in lower:
            return (
                "আপনার মন্তব্যের জন্য ধন্যবাদ। আমরা সকল নাগরিকের উদ্বেগকে গুরুত্বের সাথে বিবেচনা করি। "
                "আমাদের লক্ষ্য একটি ন্যায়সঙ্গত ও সমৃদ্ধ বাংলাদেশ গড়ে তোলা। #পরিবর্তন"
            )
        if "reel" in lower or "script" in lower:
            return (
                "SCENE 1\nVisual: Sunrise over rural Bangladesh | Text: 'নতুন ভোর' | "
                "Voiceover: বাংলাদেশ জেগে উঠছে...\n\n"
                "SCENE 2\nVisual: Crowd at rally | Text: 'একসাথে এগিয়ে যাই' | "
                "Voiceover: আপনার ভোট পরিবর্তন আনতে পারে।\n\n"
                "SCENE 3\nVisual: Candidate speaking | Text: 'ভোট দিন, পরিবর্তন আনুন' | "
                "Voiceover: আসুন একটি উজ্জ্বল ভবিষ্যৎ গড়ি।\n\n"
                "Music: Inspirational orchestral"
            )
        if "blog" in lower or "article" in lower:
            return (
                "# বাংলাদেশের রাজনৈতিক পরিবর্তন: একটি নতুন দিগন্ত\n\n"
                "## ভূমিকা\nবাংলাদেশের রাজনৈতিক পটভূমি দ্রুত পরিবর্তন হচ্ছে...\n\n"
                "## বর্তমান প্রেক্ষাপট\nজনগণ পরিবর্তন চায়...\n\n"
                "## উন্নয়নের পথে\nশিক্ষা ও স্বাস্থ্যখাতে বিনিয়োগ বাড়ানো হচ্ছে...\n\n"
                "## ভবিষ্যৎ পরিকল্পনা\nকর্মসংস্থান সৃষ্টি আমাদের মূল লক্ষ্য...\n\n"
                "## উপসংহার\nএকটি সমৃদ্ধ বাংলাদেশ গড়তে আমরা প্রতিশ্রুতিবদ্ধ।\n\n"
                "META_KEYWORDS: বাংলাদেশ রাজনীতি, পরিবর্তন, উন্নয়ন, ভোট, নেতৃত্ব"
            )
        if "xml" in lower or "blogger" in lower:
            return "<b:skin><![CDATA[/* Fixed CSS */]]></b:skin>"
        if "strategy" in lower or "strategic" in lower:
            return (
                "1. SITUATION ANALYSIS\nThe political landscape shows opportunity...\n\n"
                "2. STRATEGIC OBJECTIVES\n- Increase vote share by 15%\n- Strengthen grassroots network\n\n"
                "3. KEY MESSAGES\n- Development for all\n- Transparent governance\n\n"
                "4. ACTION PLAN\nWeek 1: Launch social campaign...\n\n"
                "5. RISK REGISTER\nRisk 1: Opposition negative campaign – Mitigation: rapid response team\n\n"
                "6. MEDIA CALENDAR\nMonday: Facebook post, Wednesday: Reel, Friday: Blog\n\n"
                "7. SUCCESS METRICS\nEngagement rate >5%, Reach >50,000/post"
            )
        return "Generated content for: " + user_prompt[:80]

    @staticmethod
    def _system_prompt(knowledge: PoliticalKnowledgeContext) -> str:
        """Build the system prompt from the knowledge context."""
        parts = [
            "You are the Political Media OS – Mahedi Engine v1, a specialised AI for "
            "political content generation and campaign strategy.",
        ]
        if knowledge.politician_name:
            parts.append(f"You are writing on behalf of {knowledge.politician_name}.")
        if knowledge.party:
            parts.append(f"Party: {knowledge.party}.")
        if knowledge.constituency:
            parts.append(f"Constituency: {knowledge.constituency}.")
        if knowledge.brand_voice:
            parts.append(f"Brand voice: {knowledge.brand_voice}.")
        if knowledge.key_messages:
            parts.append("Core messages: " + "; ".join(knowledge.key_messages) + ".")
        if knowledge.achievements:
            parts.append("Key achievements: " + "; ".join(knowledge.achievements) + ".")
        return " ".join(parts)

    @staticmethod
    def _optional_fields(command: PoliticalMediaCommand) -> str:
        """Build a formatted string of optional command fields."""
        lines = []
        if command.context:
            lines.append(f"Additional context: {command.context}")
        if command.campaign_theme:
            lines.append(f"Campaign theme: {command.campaign_theme}")
        if command.brand_voice:
            lines.append(f"Tone/voice: {command.brand_voice}")
        return ("\n".join(lines) + "\n") if lines else ""

    @staticmethod
    def _audience_line(command: PoliticalMediaCommand) -> str:
        return f"Target audience: {command.audience}\n" if command.audience else ""

    @staticmethod
    def _parse_post_response(raw: str) -> tuple[str, Optional[str], list[str]]:
        """Extract short, long, and hashtag sections from the post response."""
        short_match = re.search(r"SHORT:\s*(.*?)(?=LONG:|HASHTAGS:|$)", raw, re.DOTALL | re.IGNORECASE)
        long_match = re.search(r"LONG:\s*(.*?)(?=SHORT:|HASHTAGS:|$)", raw, re.DOTALL | re.IGNORECASE)
        hashtag_match = re.search(r"HASHTAGS:\s*(.*?)$", raw, re.DOTALL | re.IGNORECASE)

        short_text = short_match.group(1).strip() if short_match else raw.strip()
        long_text = long_match.group(1).strip() if long_match else None
        hashtags = (
            [t.strip() for t in re.split(r"[\s,]+", hashtag_match.group(1)) if t.strip().startswith("#")]
            if hashtag_match
            else []
        )
        primary = long_text or short_text
        alternate = short_text if long_text else None
        return primary, alternate, hashtags

    @staticmethod
    def _extract_hashtags(text: str) -> list[str]:
        """Extract hashtag tokens from free text."""
        return re.findall(r"#\w+", text)

    @staticmethod
    def _extract_cta(text: str) -> Optional[str]:
        """Attempt to extract the last sentence as a call-to-action."""
        sentences = [s.strip() for s in re.split(r"[।!?\n]", text) if s.strip()]
        return sentences[-1] if sentences else None

    @staticmethod
    def _extract_meta_keywords(text: str) -> list[str]:
        """Extract comma-separated keywords from a META_KEYWORDS line."""
        match = re.search(r"META_KEYWORDS:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        if not match:
            return []
        return [kw.strip() for kw in match.group(1).split(",") if kw.strip()]

    @staticmethod
    def _validate_xml_syntax(xml_string: str) -> dict[str, Any]:
        """Attempt to parse the XML and return a validation report.

        Args:
            xml_string: Raw XML text to validate.

        Returns:
            Dictionary with keys ``valid`` (bool) and ``errors`` (list[str]).
        """
        if not xml_string.strip():
            return {"valid": False, "errors": ["Empty XML input."]}
        try:
            ET.fromstring(xml_string)
            return {"valid": True, "errors": []}
        except ET.ParseError as exc:
            return {"valid": False, "errors": [str(exc)]}
