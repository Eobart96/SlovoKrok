from pathlib import Path
import shutil
import subprocess

import pytest

from app.config import Settings
import app.tutor_providers.codex as tutor_module
from app.tutor import CodexCliProvider, TutorContext, TutorProviderTimeout, build_tutor_context


def _settings(tmp_path: Path, **overrides) -> Settings:
    project_root = tmp_path / "project"
    project_root.mkdir(exist_ok=True)
    defaults = {
        "project_root": project_root,
        "learning_path": Path(__file__).parents[2] / "course-content" / "slovak-a1" / "learning",
        "codex_command": "codex.exe",
    }
    defaults.update(overrides)
    return Settings(**defaults)


def test_codex_response_runs_in_empty_temporary_workspace_and_cleans_it(tmp_path: Path, monkeypatch):
    settings = _settings(tmp_path)
    executable = tmp_path / "codex.exe"
    executable.touch()
    captured: dict[str, Path] = {}
    monkeypatch.setattr(tutor_module, "resolve_codex_executable", lambda _: executable)

    def fake_run(command, *, cwd, **kwargs):
        workspace = Path(cwd)
        captured["workspace"] = workspace
        assert workspace != settings.project_root
        assert list(workspace.iterdir()) == []
        assert command[1:6] == ["exec", "--ephemeral", "-s", "read-only", "--skip-git-repo-check"]
        assert kwargs["input"] == b"test prompt"
        output_path = Path(command[command.index("-o") + 1])
        assert output_path.parent != workspace
        output_path.write_text('{"answer":"ok"}', encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(tutor_module.subprocess, "run", fake_run)

    response = CodexCliProvider(settings).respond(TutorContext(prompt="test prompt"))

    assert response == '{"answer":"ok"}'
    assert not captured["workspace"].exists()


def test_codex_response_cleans_workspace_after_timeout(tmp_path: Path, monkeypatch):
    settings = _settings(tmp_path)
    executable = tmp_path / "codex.exe"
    executable.touch()
    captured: dict[str, Path] = {}
    monkeypatch.setattr(tutor_module, "resolve_codex_executable", lambda _: executable)

    def timeout_run(command, *, cwd, **kwargs):
        captured["workspace"] = Path(cwd)
        raise subprocess.TimeoutExpired(command, settings.tutor_timeout_seconds)

    monkeypatch.setattr(tutor_module.subprocess, "run", timeout_run)

    with pytest.raises(TutorProviderTimeout):
        CodexCliProvider(settings).respond(TutorContext(prompt="test prompt"))

    assert not captured["workspace"].exists()


def test_codex_status_uses_isolated_workspace(tmp_path: Path, monkeypatch):
    settings = _settings(tmp_path)
    executable = tmp_path / "codex.exe"
    executable.touch()
    captured: dict[str, Path] = {}
    monkeypatch.setattr(tutor_module, "resolve_codex_executable", lambda _: executable)

    def fake_run(command, *, cwd, **kwargs):
        workspace = Path(cwd)
        captured["workspace"] = workspace
        assert workspace != settings.project_root
        assert list(workspace.iterdir()) == []
        return subprocess.CompletedProcess(command, 0, stdout=b"Logged in", stderr=b"")

    monkeypatch.setattr(tutor_module.subprocess, "run", fake_run)

    status = tutor_module.get_codex_connection_status(settings)

    assert status.authenticated is True
    assert not captured["workspace"].exists()


def test_codex_login_uses_isolated_workspace_and_schedules_cleanup(tmp_path: Path, monkeypatch):
    settings = _settings(tmp_path)
    executable = tmp_path / "codex.exe"
    executable.touch()
    captured: dict[str, Path] = {}
    fake_process = object()
    monkeypatch.setattr(
        tutor_module,
        "get_codex_connection_status",
        lambda _: tutor_module.CodexConnectionStatus(True, False, "login required"),
    )
    monkeypatch.setattr(tutor_module, "resolve_codex_executable", lambda _: executable)

    def fake_popen(command, *, cwd, **kwargs):
        workspace = Path(cwd)
        captured["workspace"] = workspace
        assert workspace != settings.project_root
        assert list(workspace.iterdir()) == []
        return fake_process

    def fake_cleanup(process, workspace):
        assert process is fake_process
        captured["cleanup"] = workspace
        shutil.rmtree(workspace)

    monkeypatch.setattr(tutor_module.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(tutor_module, "_schedule_codex_workspace_cleanup", fake_cleanup)

    status = tutor_module.start_codex_login(settings)

    assert status.installed is True
    assert captured["cleanup"] == captured["workspace"]
    assert not captured["workspace"].exists()


def test_private_profile_requires_explicit_opt_in(tmp_path: Path):
    settings = _settings(tmp_path, share_private_tutor_profile=True)
    local_profile = settings.project_root / ".ai" / "private" / "student_profile.local.md"
    local_profile.parent.mkdir(parents=True)
    local_profile.write_text("Локальная настройка ученика.", encoding="utf-8")

    context = build_tutor_context(settings, "Начнём урок")

    assert "Локальная настройка ученика." in context.prompt
    assert "Это публичный пример профиля" not in context.prompt


def test_codex_login_failure_removes_workspace(tmp_path: Path, monkeypatch):
    settings = _settings(tmp_path)
    executable = tmp_path / "codex.exe"
    executable.touch()
    captured: dict[str, Path] = {}
    monkeypatch.setattr(
        tutor_module,
        "get_codex_connection_status",
        lambda _: tutor_module.CodexConnectionStatus(True, False, "login required"),
    )
    monkeypatch.setattr(tutor_module, "resolve_codex_executable", lambda _: executable)

    def failing_popen(command, *, cwd, **kwargs):
        captured["workspace"] = Path(cwd)
        raise OSError("test failure")

    monkeypatch.setattr(tutor_module.subprocess, "Popen", failing_popen)

    with pytest.raises(RuntimeError, match="Не удалось запустить вход"):
        tutor_module.start_codex_login(settings)

    assert not captured["workspace"].exists()
