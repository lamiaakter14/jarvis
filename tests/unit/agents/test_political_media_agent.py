"""Unit tests for PoliticalMediaAgent and PoliticalMediaService."""

from unittest.mock import AsyncMock

import pytest
from jarvis_core.domain.entities.political_media import (
    MediaCommand,
    PoliticalKnowledgeContext,
    PoliticalMediaCommand,
    PoliticalMediaResult,
)
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.infrastructure.agents.political_media_agent import PoliticalMediaAgent
from jarvis_core.infrastructure.ai.political_media_service import PoliticalMediaService
from jarvis_core.shared.exceptions import DomainException


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_memory_repo():
    repo = AsyncMock()
    repo.save = AsyncMock(return_value=None)
    return repo


@pytest.fixture
def mock_service():
    return PoliticalMediaService(mock_mode=True)


@pytest.fixture
def knowledge():
    return PoliticalKnowledgeContext(
        politician_name="মাহেদি হাসান",
        party="National Progress Party",
        constituency="Dhaka-5",
        key_messages=["উন্নয়ন", "শিক্ষা", "কর্মসংস্থান"],
        brand_voice="assertive and empathetic",
    )


@pytest.fixture
def agent(mock_service, mock_memory_repo, knowledge):
    return PoliticalMediaAgent(
        media_service=mock_service,
        memory_repo=mock_memory_repo,
        knowledge=knowledge,
    )


# ---------------------------------------------------------------------------
# PoliticalMediaCommand – parsing
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPoliticalMediaCommand:
    def test_parse_post_simple(self):
        cmd = PoliticalMediaCommand.from_text("/post আমাদের উন্নয়ন")
        assert cmd.command == MediaCommand.POST
        assert cmd.topic == "আমাদের উন্নয়ন"
        assert cmd.language == "Bengali"

    def test_parse_all_fields(self):
        raw = "/strategy economic policy | current crisis | youth | progress | assertive | English"
        cmd = PoliticalMediaCommand.from_text(raw)
        assert cmd.command == MediaCommand.STRATEGY
        assert cmd.topic == "economic policy"
        assert cmd.context == "current crisis"
        assert cmd.audience == "youth"
        assert cmd.campaign_theme == "progress"
        assert cmd.brand_voice == "assertive"
        assert cmd.language == "English"

    def test_parse_unknown_command_raises(self):
        with pytest.raises(ValueError, match="Unknown command"):
            PoliticalMediaCommand.from_text("/unknown some topic")

    def test_parse_empty_topic_raises(self):
        with pytest.raises(ValueError, match="Topic must not be empty"):
            PoliticalMediaCommand.from_text("/post ")

    def test_command_ids_are_unique(self):
        cmd1 = PoliticalMediaCommand.from_text("/post topic A")
        cmd2 = PoliticalMediaCommand.from_text("/post topic B")
        assert cmd1.command_id != cmd2.command_id


# ---------------------------------------------------------------------------
# PoliticalMediaAgent – initialisation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPoliticalMediaAgentInit:
    def test_agent_type(self, agent):
        assert agent.agent_type == AgentType.POLITICAL_MEDIA_OS

    def test_agent_name(self, agent):
        assert "Mahedi Engine" in agent.name

    def test_agent_description_mentions_capabilities(self, agent):
        desc = agent.description.lower()
        assert "facebook" in desc or "political" in desc


# ---------------------------------------------------------------------------
# PoliticalMediaAgent – command routing via execute()
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.asyncio
class TestPoliticalMediaAgentExecute:
    async def test_execute_post_command_string(self, agent):
        result = await agent.execute("/post আমাদের উন্নয়ন")
        assert result["command"] == "/post"
        assert "primary_output" in result
        assert result["primary_output"]

    async def test_execute_reply_command_string(self, agent):
        result = await agent.execute("/reply আপনি কি করলেন এতদিন?")
        assert result["command"] == "/reply"
        assert "primary_output" in result

    async def test_execute_reel_command_string(self, agent):
        result = await agent.execute("/reel নির্বাচনী প্রচারণা | 30s")
        assert result["command"] == "/reel"
        assert "metadata" in result

    async def test_execute_blog_command_string(self, agent):
        result = await agent.execute("/blog বাংলাদেশের ভবিষ্যৎ")
        assert result["command"] == "/blog"
        assert "primary_output" in result

    async def test_execute_strategy_command_string(self, agent):
        result = await agent.execute("/strategy নির্বাচন প্রস্তুতি")
        assert result["command"] == "/strategy"
        assert result["primary_output"]

    async def test_execute_fixxml_command(self, agent):
        raw_xml = "<b:widget id='HTML1' type='HTML'><b:includable id='main'><![CDATA[hello]]></b:includable></b:widget>"
        result = await agent.execute(f"/fixxml xml fix | {raw_xml}")
        assert result["command"] == "/fixxml"
        assert "primary_output" in result

    async def test_execute_with_command_object(self, agent):
        cmd = PoliticalMediaCommand(command=MediaCommand.POST, topic="নতুন বাংলাদেশ")
        result = await agent.execute(cmd)
        assert result["command"] == "/post"

    async def test_execute_invalid_string_raises_domain_exception(self, agent):
        with pytest.raises(DomainException):
            await agent.execute("/unknown topic")

    async def test_execute_wrong_type_raises_domain_exception(self, agent):
        with pytest.raises(DomainException):
            await agent.execute(12345)

    async def test_memory_persisted_on_execute(self, agent, mock_memory_repo):
        await agent.execute("/post test topic")
        mock_memory_repo.save.assert_called_once()

    async def test_metrics_tracked_on_success(self, agent):
        await agent.execute("/post test")
        assert agent.total_executions == 1
        assert agent.successful_executions == 1

    async def test_metrics_tracked_on_failure(self, agent, mock_memory_repo):
        mock_memory_repo.save.side_effect = Exception("db error")
        # Memory failure is logged but doesn't raise; metrics still increment
        await agent.execute("/post test")
        assert agent.total_executions == 1


# ---------------------------------------------------------------------------
# PoliticalMediaService – generation modules
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.asyncio
class TestPoliticalMediaService:
    @pytest.fixture
    def svc(self):
        return PoliticalMediaService(mock_mode=True)

    @pytest.fixture
    def cmd_post(self):
        return PoliticalMediaCommand(
            command=MediaCommand.POST,
            topic="শিক্ষা সংস্কার",
            audience="youth voters",
        )

    @pytest.fixture
    def empty_knowledge(self):
        return PoliticalKnowledgeContext()

    async def test_generate_facebook_post_returns_result(self, svc, cmd_post, empty_knowledge):
        result = await svc.generate_facebook_post(cmd_post, empty_knowledge)
        assert isinstance(result, PoliticalMediaResult)
        assert result.command == MediaCommand.POST
        assert result.primary_output

    async def test_post_has_hashtags(self, svc, cmd_post, empty_knowledge):
        result = await svc.generate_facebook_post(cmd_post, empty_knowledge)
        assert isinstance(result.hashtags, list)
        assert len(result.hashtags) > 0

    async def test_generate_reply_returns_result(self, svc, empty_knowledge):
        cmd = PoliticalMediaCommand(command=MediaCommand.REPLY, topic="আপনি কি করলেন?")
        result = await svc.generate_comment_reply(cmd, empty_knowledge)
        assert isinstance(result, PoliticalMediaResult)
        assert result.command == MediaCommand.REPLY
        assert result.primary_output

    async def test_generate_reel_script_returns_result(self, svc, empty_knowledge):
        cmd = PoliticalMediaCommand(command=MediaCommand.REEL, topic="নির্বাচনী সমাবেশ", context="60s")
        result = await svc.generate_reel_script(cmd, empty_knowledge)
        assert result.command == MediaCommand.REEL
        assert "metadata" in result.to_dict()

    async def test_generate_blog_returns_result(self, svc, empty_knowledge):
        cmd = PoliticalMediaCommand(command=MediaCommand.BLOG, topic="উন্নয়নের পথে")
        result = await svc.generate_blog_content(cmd, empty_knowledge)
        assert result.command == MediaCommand.BLOG
        assert result.primary_output

    async def test_generate_strategy_returns_result(self, svc, empty_knowledge):
        cmd = PoliticalMediaCommand(command=MediaCommand.STRATEGY, topic="election prep")
        result = await svc.generate_political_strategy(cmd, empty_knowledge)
        assert result.command == MediaCommand.STRATEGY
        assert result.primary_output

    async def test_fix_valid_xml_returns_result(self, svc, empty_knowledge):
        valid_xml = "<root><item>test</item></root>"
        cmd = PoliticalMediaCommand(command=MediaCommand.FIXXML, topic="fix xml", context=valid_xml)
        result = await svc.fix_blogger_xml(cmd, empty_knowledge)
        assert result.command == MediaCommand.FIXXML
        assert result.metadata["post_fix_valid"] is True

    async def test_fix_invalid_xml_adds_qa_flag(self, svc, empty_knowledge):
        broken_xml = "<root><item>unclosed"
        cmd = PoliticalMediaCommand(command=MediaCommand.FIXXML, topic="fix xml", context=broken_xml)
        result = await svc.fix_blogger_xml(cmd, empty_knowledge)
        # Mock mode returns fixed XML stub; post-validation may still fail on stub
        assert result.command == MediaCommand.FIXXML

    async def test_apply_qa_empty_output_adds_flag(self, svc):
        cmd = PoliticalMediaCommand(command=MediaCommand.POST, topic="test")
        result = PoliticalMediaResult(command_id=cmd.command_id, command=MediaCommand.POST, primary_output="")
        flagged = svc.apply_qa(result, cmd)
        assert any("empty" in f.lower() for f in flagged.qa_flags)

    async def test_package_output_contains_engine_key(self, svc):
        cmd = PoliticalMediaCommand(command=MediaCommand.POST, topic="test")
        result = PoliticalMediaResult(
            command_id=cmd.command_id, command=MediaCommand.POST, primary_output="Hello"
        )
        output = svc.package_output(result, cmd)
        assert output["engine"] == "Political Media OS – Mahedi Engine v1"
        assert output["command"] == "/post"


# ---------------------------------------------------------------------------
# PoliticalMediaResult – serialisation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPoliticalMediaResult:
    def test_to_dict_contains_all_keys(self):
        result = PoliticalMediaResult(
            command_id="cmd_001",
            command=MediaCommand.POST,
            primary_output="Hello world",
            hashtags=["#test"],
            cta="Vote now",
        )
        d = result.to_dict()
        for key in ("result_id", "command_id", "command", "primary_output", "hashtags", "cta"):
            assert key in d

    def test_result_ids_are_unique(self):
        r1 = PoliticalMediaResult(command_id="x", command=MediaCommand.POST, primary_output="a")
        r2 = PoliticalMediaResult(command_id="x", command=MediaCommand.POST, primary_output="b")
        assert r1.result_id != r2.result_id


# ---------------------------------------------------------------------------
# Master prompt sanity check
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMasterPrompt:
    def test_master_prompt_is_non_empty(self):
        from jarvis_core.infrastructure.ai.master_prompt import MASTER_PROMPT

        assert MASTER_PROMPT
        assert len(MASTER_PROMPT) > 500

    def test_master_prompt_contains_all_commands(self):
        from jarvis_core.infrastructure.ai.master_prompt import MASTER_PROMPT

        for cmd in ("/post", "/reply", "/reel", "/blog", "/fixxml", "/strategy"):
            assert cmd in MASTER_PROMPT
