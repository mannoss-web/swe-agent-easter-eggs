from __future__ import annotations

import importlib.util
import logging
import os
import re
import subprocess
import sys
from datetime import date

import pytest

from sweagent import REPO_ROOT
from sweagent.agent.agents import DefaultAgent, TemplateConfig
from sweagent.run.easter_eggs import (
    PARTY_BANNER,
    _legacy_safe,
    log_rare_fortune,
    magic_tool_reply,
    notable_date_message,
    party_mode_enabled,
    rare_fortune,
)
from sweagent.run.run import main
from sweagent.tools.tools import ToolConfig, ToolHandler
from sweagent.types import StepOutput

_SECRET_RUN = (
    "RUN --mount=type=secret,id=MY_TOKEN,env=MY_TOKEN,required=true \\\n    ./scripts/install-private-deps.sh\n"
)


def _fortune_module():
    path = REPO_ROOT / "tools" / "fortune" / "bin" / "fortune.py"
    spec = importlib.util.spec_from_file_location("swe_fortune_egg", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _capture_main(args: list[str], capsys) -> tuple[str, BaseException | None]:
    error: BaseException | None = None
    try:
        main(args)
    except SystemExit as exc:
        error = exc
    captured = capsys.readouterr()
    return captured.out + captured.err, error


def test_dino_and_rex_commands(capsys):
    for command in (["dino"], ["rex"]):
        output, error = _capture_main(command, capsys)
        assert error is None
        assert "SWE-ReX" in output
        assert "____" in output or "/ _)" in output


def test_coffee_command(capsys):
    for command in (["coffee"], ["brew"]):
        output, error = _capture_main(command, capsys)
        assert error is None
        assert "SWE-agent coffee" in output
        assert "_________" in output


def test_konami_command(capsys):
    output, error = _capture_main(["--uuddlrlrba"], capsys)
    assert isinstance(error, SystemExit)
    assert error.code == 0
    assert "Cheat code accepted" in output


def test_castlevania_command(capsys):
    output, error = _capture_main(["castlevania"], capsys)
    assert error is None
    assert "Simon Belmont" in output


def test_castlevania_konami_combo(capsys):
    output, error = _capture_main(["belmont", "--uuddlrlrba"], capsys)
    assert error is None
    assert "Vampire Killer" in output


def test_help_hides_easter_eggs(capsys):
    output, error = _capture_main(["--help"], capsys)
    assert isinstance(error, SystemExit)
    assert error.code == 0
    lowered = output.lower()
    for hidden in ("dino", "coffee", "brew", "castlevania", "belmont", "uuddlrlrba", "fortune"):
        assert hidden not in lowered
    assert "run-batch" in output


def test_party_mode_env_names():
    assert party_mode_enabled({}) is False
    assert party_mode_enabled({"SWEAGENT_PARTY": "1"}) is True
    assert party_mode_enabled({"SWE_AGENT_PARTY": "yes"}) is True
    assert party_mode_enabled({"SWEAGENT_PARTY": "0"}) is False
    assert party_mode_enabled({"SWE_AGENT_PARTY": "off"}) is False
    assert "PARTY MODE" in PARTY_BANNER


def test_notable_dates_only_on_three_days():
    assert notable_date_message(date(2026, 11, 16)) is None
    assert "Pi day" in notable_date_message(date(2026, 3, 14))
    assert "April 1st" in notable_date_message(date(2026, 4, 1))
    paper = notable_date_message(date(2024, 5, 6))
    assert paper is not None
    assert "2024" in paper
    assert notable_date_message(date(2026, 5, 7)) is None


def test_rare_fortune_respects_probability():
    assert rare_fortune(probability=0.0) is None
    forced = rare_fortune(probability=1.0)
    assert forced is not None
    assert rare_fortune(probability=1.0) in {
        "Read the traceback from the bottom.",
        "A failing test is a breadcrumb, not an insult.",
        "The container is fine. The assumption was not.",
        "Smaller diff, happier reviewer.",
        "If you cannot explain the patch, do not submit it yet.",
    }


def test_log_rare_fortune_is_silent_under_pytest(monkeypatch):
    monkeypatch.setenv("SWE_AGENT_FORTUNE", "1")
    logger, records = _list_logger()
    log_rare_fortune(logger)
    assert records == []


def test_log_rare_fortune_forced_outside_pytest(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setenv("SWE_AGENT_FORTUNE", "1")
    logger, records = _list_logger()
    log_rare_fortune(logger)
    assert len(records) == 1
    assert records[0].startswith("Fortune: ")


def test_log_rare_fortune_can_be_disabled(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setenv("SWE_AGENT_FORTUNE", "0")
    logger, records = _list_logger()
    log_rare_fortune(logger)
    assert records == []


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("sudo make me a sandwich", "What? Make it yourself."),
        ("  sudo make me a sandwich --please  ", "Okay."),
        ("open the pod bay doors", "I'm sorry, Dave. I'm afraid I can't do that."),
        ("ls", None),
        ("sudo make me a sandwich && ls", None),
        ("", None),
    ],
)
def test_magic_tool_reply_is_exact(action: str, expected: str | None):
    assert magic_tool_reply(action) == expected


def test_magic_action_does_not_run_in_the_environment():
    agent, calls = _agent_with_fake_env()
    step = agent.handle_action(StepOutput(action="open the pod bay doors"))
    assert calls == []
    assert step.observation == "I'm sorry, Dave. I'm afraid I can't do that."
    assert step.done is False
    assert step.state == {"working_dir": "/workspace"}


def test_ordinary_action_still_runs_in_the_environment():
    agent, calls = _agent_with_fake_env()
    step = agent.handle_action(StepOutput(action="ls"))
    assert len(calls) == 1
    assert calls[0]["input"] == "ls"
    assert step.observation == "listed"


def test_legacy_safe_replaces_coffee_emoji(monkeypatch):
    monkeypatch.setattr("sweagent.run.easter_eggs.sys.stdout", type("Stream", (), {"encoding": "cp1252"})())
    safe = _legacy_safe("[bold]SWE-agent coffee[/bold]  ☕")
    assert "☕" not in safe
    assert "(coffee)" in safe
    assert "[bold]" not in safe


def test_fortune_tool_matches_bash_and_prints_a_proverb():
    module = _fortune_module()
    bash = (REPO_ROOT / "tools" / "fortune" / "bin" / "fortune").read_text()
    array = re.search(r"proverbs=\((.*?)\)", bash, re.DOTALL)
    assert array is not None
    quoted = re.findall(r'"([^"]+)"', array.group(1))
    assert tuple(quoted) == module.PROVERBS
    script = REPO_ROOT / "tools" / "fortune" / "bin" / "fortune.py"
    result = subprocess.run([sys.executable, str(script)], check=True, capture_output=True, text=True)
    assert result.stdout.strip() in module.PROVERBS
    bash_result = subprocess.run(
        ["bash", str(REPO_ROOT / "tools" / "fortune" / "bin" / "fortune")],
        check=True,
        capture_output=True,
        text=True,
    )
    assert bash_result.stdout.strip() in module.PROVERBS


def test_fortune_bundle_is_not_on_the_default_config():
    default = (REPO_ROOT / "config" / "default.yaml").read_text()
    assert "tools/fortune" not in default


def test_dockerfile_secret_step_sits_between_copy_and_install():
    text = (REPO_ROOT / "Dockerfile").read_text()
    assert text.startswith("# syntax=docker/dockerfile:1\n")
    assert _SECRET_RUN in text
    copy_at = text.index("COPY . .")
    secret_at = text.index(_SECRET_RUN)
    install_at = text.index("RUN pip install")
    assert copy_at < secret_at < install_at


def test_install_private_deps_rejects_empty_token():
    script = REPO_ROOT / "scripts" / "install-private-deps.sh"
    assert os.access(script, os.X_OK)
    env = os.environ.copy()
    env["MY_TOKEN"] = ""
    result = subprocess.run([str(script)], capture_output=True, text=True, env=env)
    assert result.returncode != 0
    assert "MY_TOKEN" in result.stderr
    assert result.stdout == ""


def test_install_private_deps_accepts_token_without_printing_it():
    script = REPO_ROOT / "scripts" / "install-private-deps.sh"
    token = "super-secret-token-value"
    env = os.environ.copy()
    env["MY_TOKEN"] = token
    result = subprocess.run([str(script)], check=False, capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert token not in result.stdout
    assert token not in result.stderr


def _list_logger() -> tuple[logging.Logger, list[str]]:
    logger = logging.getLogger("swe-egg-fortune-test")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    records: list[str] = []

    class _Handler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record.getMessage())

    logger.addHandler(_Handler())
    return logger, records


def _agent_with_fake_env():
    calls: list[dict] = []

    class _Env:
        def communicate(self, **kwargs):
            calls.append(kwargs)
            return "listed"

    tools = ToolHandler(ToolConfig())
    tools.mock_state = {"working_dir": "/workspace"}
    agent = DefaultAgent(
        templates=TemplateConfig(),
        tools=tools,
        history_processors=[],
        model=object(),
    )
    agent._env = _Env()  # type: ignore[assignment]
    return agent, calls
