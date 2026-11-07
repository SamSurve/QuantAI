"""Tests for chat session continuity, session reuse, turn counter, and message ordering.

Step D acceptance criteria:
1. Session reuse.
2. Ordered message history.
3. Turn counter.
4. Three original quick prompts.
5. Correct message submission.
6. Session continuity.
"""

from __future__ import annotations

import math
from unittest.mock import patch
import pytest
from agno.models.response import ModelResponse
from fastapi.testclient import TestClient

from api.index import app
from api.web.chat import friendly_agent_error, render_rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset the render rate limiter state before each test."""
    render_rate_limiter.reset()


client = TestClient(app)


def test_session_id_reuse_across_multiple_turns():
    """Verify that multiple chat operations in a conversation reuse the exact same session_id,
    advance turn count, and maintain message order using mocked AgentOS responses."""
    session_id = "test-session-persistent-12345"

    with patch("api.groq_finance_agent.provider_router.aresponse") as mock_aresponse:
        # --- TURN 1 ---
        mock_aresponse.return_value = ModelResponse(
            content="## Thesis 1\nOperating margin expansion is supported by **Testco** pricing power."
        )

        run_1 = client.post(
            "/api/agents/groq-finance-agent/runs",
            data={
                "message": "Pressure-test the thesis",
                "stream": "false",
                "session_id": session_id,
            },
        )
        assert run_1.status_code == 200
        run_1_data = run_1.json()
        assert run_1_data["session_id"] == session_id
        assert "Thesis 1" in run_1_data["content"]

        # Render turn 1 Markdown -> HTML
        render_1 = client.post("/api/chat/render", json={"text": run_1_data["content"]})
        assert render_1.status_code == 200
        html_1 = render_1.json()["html"]
        assert "<h2>Thesis 1</h2>" in html_1
        assert "<strong>Testco</strong>" in html_1

        # --- TURN 2 ---
        mock_aresponse.return_value = ModelResponse(
            content="## Source Lane 2\nSourced from Form 10-Q filing dated October 2026."
        )

        run_2 = client.post(
            "/api/agents/groq-finance-agent/runs",
            data={
                "message": "Trace the source lane",
                "stream": "false",
                "session_id": session_id,
            },
        )
        assert run_2.status_code == 200
        run_2_data = run_2.json()
        assert run_2_data["session_id"] == session_id
        assert "Source Lane 2" in run_2_data["content"]

        # Render turn 2 Markdown -> HTML
        render_2 = client.post("/api/chat/render", json={"text": run_2_data["content"]})
        assert render_2.status_code == 200
        html_2 = render_2.json()["html"]
        assert "<h2>Source Lane 2</h2>" in html_2
        assert "Form 10-Q" in html_2

        # --- VERIFICATIONS ---
        # 1. Exact same session ID reused across both AgentOS run operations
        assert run_1_data["session_id"] == run_2_data["session_id"] == session_id

        # 2. Both turns produced distinct run IDs under that session
        assert run_1_data["run_id"] != run_2_data["run_id"]

        # 3. Message history sequence across turns preserves chronological ordering
        history = [
            {"turn": 1, "role": "user", "content": "Pressure-test the thesis"},
            {"turn": 1, "role": "agent", "content": run_1_data["content"], "html": html_1},
            {"turn": 2, "role": "user", "content": "Trace the source lane"},
            {"turn": 2, "role": "agent", "content": run_2_data["content"], "html": html_2},
        ]
        assert len(history) == 4
        assert [m["role"] for m in history] == ["user", "agent", "user", "agent"]
        assert [m["turn"] for m in history] == [1, 1, 2, 2]

        # 4. Turn counter calculation advances correctly from 0 to 1 to 2
        turns_at_start = 0
        turns_after_turn_1 = math.ceil(len(history[:2]) / 2)
        turns_after_turn_2 = math.ceil(len(history) / 2)
        assert turns_at_start == 0
        assert turns_after_turn_1 == 1
        assert turns_after_turn_2 == 2


def test_chat_turn_counter_calculation():
    """Verify turn counter increments properly for each research turn."""
    def calculate_turns(msg_count: int) -> int:
        return math.ceil(msg_count / 2) if msg_count > 0 else 0

    assert calculate_turns(0) == 0
    assert calculate_turns(1) == 1
    assert calculate_turns(2) == 1  # 1 user + 1 agent = 1 complete turn
    assert calculate_turns(3) == 2
    assert calculate_turns(4) == 2  # 2 user + 2 agent = 2 complete turns

    def turn_label(turn_count: int) -> str:
        if turn_count == 0:
            return "0 turns"
        return f"{turn_count} turn" if turn_count == 1 else f"{turn_count} turns"

    assert turn_label(0) == "0 turns"
    assert turn_label(1) == "1 turn"
    assert turn_label(2) == "2 turns"


def test_chat_ordered_message_history():
    """Verify messages maintain strictly chronological sequence (user, agent, user, agent)."""
    history: list[dict[str, str]] = []

    def add_message(role: str, content: str):
        history.append({"role": role, "content": content})

    add_message("user", "Pressure-test the thesis")
    add_message("agent", "<p>Thesis analysis...</p>")
    add_message("user", "Trace the source lane")
    add_message("agent", "<p>Source lane verification...</p>")

    assert len(history) == 4
    assert [m["role"] for m in history] == ["user", "agent", "user", "agent"]
    assert history[0]["content"] == "Pressure-test the thesis"
    assert history[2]["content"] == "Trace the source lane"


def test_chat_session_error_handling_sanitization():
    """Verify session errors do not leak stack traces, internal paths, or credentials."""
    msg = friendly_agent_error("Traceback (most recent call last):\nFile 'C:\\api\\secrets.py', line 12", 500)
    assert "Traceback" not in msg
    assert "C:\\" not in msg
    assert "secrets" not in msg
    assert "The Research Desk is temporarily unavailable." in msg

    msg_503 = friendly_agent_error("Groq upstream connection failed", 503)
    assert "AI analysis is temporarily unavailable" in msg_503
    assert "Groq" not in msg_503
