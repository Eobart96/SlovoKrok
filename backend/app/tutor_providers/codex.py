from contextlib import contextmanager
from dataclasses import dataclass
import os
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
from typing import Iterator

from app.config import Settings
from app.tutor_core.contracts import (
    MAX_AI_RESPONSE_BYTES,
    AIResponseError,
    TutorContext,
    TutorProviderError,
    TutorProviderTimeout,
)


class CodexCliProvider:
    """Use the locally authenticated Codex CLI subscription in read-only mode."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def respond(self, context: TutorContext) -> str:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as output_file:
            output_path = Path(output_file.name)

        executable_path = resolve_codex_executable(self.settings.codex_command)
        if executable_path is None:
            raise RuntimeError("Codex CLI не установлен или не найден.")
        command = _codex_process_args(
            executable_path,
            ["exec", "--ephemeral", "-s", "read-only", "--skip-git-repo-check", "-o", str(output_path)],
        )
        schema_path = None
        try:
            if context.response_schema is not None:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as schema_file:
                    schema_path = Path(schema_file.name)
                    json.dump(context.response_schema, schema_file, ensure_ascii=False)
                command.extend(["--output-schema", str(schema_path)])
            try:
                with _temporary_codex_workspace(self.settings.project_root) as workspace:
                    result = subprocess.run(
                        command,
                        input=context.prompt.encode("utf-8"),
                        capture_output=True,
                        cwd=workspace,
                        timeout=self.settings.tutor_timeout_seconds,
                        check=False,
                    )
            except subprocess.TimeoutExpired as error:
                raise TutorProviderTimeout("Codex CLI timed out") from error
            except OSError as error:
                raise TutorProviderError("Codex CLI could not be started") from error
            if result.returncode != 0:
                detail = (
                    _decode_process_output(result.stderr).strip()
                    or _decode_process_output(result.stdout).strip()
                    or "Unknown Codex error"
                )
                raise TutorProviderError(detail)
            if output_path.stat().st_size > MAX_AI_RESPONSE_BYTES:
                raise AIResponseError("Codex response exceeds the allowed byte size")
            try:
                response = output_path.read_text(encoding="utf-8").strip()
            except UnicodeError as error:
                raise AIResponseError("Codex response is not valid UTF-8") from error
            if not response:
                raise AIResponseError("Codex returned an empty response")
            return response
        finally:
            output_path.unlink(missing_ok=True)
            if schema_path is not None:
                schema_path.unlink(missing_ok=True)


@dataclass(frozen=True)
class CodexConnectionStatus:
    installed: bool
    authenticated: bool
    message: str


def _validate_codex_workspace(workspace: Path, project_root: Path) -> Path:
    resolved_workspace = workspace.resolve()
    try:
        resolved_workspace.relative_to(project_root.resolve())
    except ValueError:
        pass
    else:
        raise RuntimeError("Изолированная рабочая папка Codex не может находиться внутри проекта.")
    if any(resolved_workspace.iterdir()):
        raise RuntimeError("Изолированная рабочая папка Codex должна быть пустой.")
    return resolved_workspace


@contextmanager
def _temporary_codex_workspace(project_root: Path) -> Iterator[Path]:
    """Create an empty, short-lived cwd outside the project for a Codex command."""
    with tempfile.TemporaryDirectory(prefix="slovokrok-codex-") as directory:
        yield _validate_codex_workspace(Path(directory), project_root)


def _create_codex_login_workspace(project_root: Path) -> Path:
    workspace = Path(tempfile.mkdtemp(prefix="slovokrok-codex-login-"))
    try:
        return _validate_codex_workspace(workspace, project_root)
    except Exception:
        shutil.rmtree(workspace, ignore_errors=True)
        raise


def _schedule_codex_workspace_cleanup(process: subprocess.Popen, workspace: Path) -> None:
    """Remove an interactive login cwd after the child process has exited."""
    def wait_and_remove() -> None:
        try:
            process.wait()
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

    threading.Thread(
        target=wait_and_remove,
        name="slovokrok-codex-workspace-cleanup",
        daemon=True,
    ).start()


def resolve_codex_executable(configured_command: str) -> Path | None:
    """Resolve Codex from PATH, an explicit setting, npm, or the desktop app."""
    configured_path = Path(configured_command).expanduser()
    if configured_path.is_file():
        return configured_path.resolve()

    path_match = shutil.which(configured_command)
    if path_match:
        return Path(path_match).resolve()

    candidates: list[Path] = []
    candidates.append(Path(__file__).resolve().parents[3] / "frontend" / "node_modules" / ".bin" / "codex.cmd")
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "codex.cmd")

    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        desktop_bin = Path(local_appdata) / "OpenAI" / "Codex" / "bin"
        if desktop_bin.is_dir():
            candidates.extend(desktop_bin.glob("*/codex.exe"))
        candidates.append(Path(local_appdata) / "Microsoft" / "WinGet" / "Links" / "codex.exe")

    existing = [candidate for candidate in candidates if candidate.is_file()]
    if not existing:
        return None
    return max(existing, key=lambda candidate: candidate.stat().st_mtime).resolve()


def _codex_process_args(executable: Path, arguments: list[str]) -> list[str]:
    """Bypass cmd quoting by running the npm Codex entrypoint with Node directly."""
    if executable.suffix.lower() in {".cmd", ".bat"}:
        codex_js = executable.parent.parent / "@openai" / "codex" / "bin" / "codex.js"
        node_executable = shutil.which("node")
        if codex_js.is_file() and node_executable:
            return [node_executable, str(codex_js), *arguments]
    return [str(executable), *arguments]


def get_codex_connection_status(settings: Settings) -> CodexConnectionStatus:
    """Check whether the configured Codex CLI is available and authenticated."""
    executable = resolve_codex_executable(settings.codex_command)
    if not executable:
        return CodexConnectionStatus(False, False, "Codex CLI не установлен или не найден.")

    command = _codex_process_args(executable, ["login", "status"])
    try:
        with _temporary_codex_workspace(settings.project_root) as workspace:
            result = subprocess.run(
                command,
                capture_output=True,
                cwd=workspace,
                timeout=15,
                check=False,
            )
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        return CodexConnectionStatus(True, False, f"Не удалось проверить авторизацию Codex: {error}")

    output = _decode_process_output(result.stdout).strip() or _decode_process_output(result.stderr).strip()
    if result.returncode == 0:
        return CodexConnectionStatus(True, True, output or "Codex подключён.")
    return CodexConnectionStatus(True, False, output or "Требуется вход в Codex.")


def start_codex_login(settings: Settings) -> CodexConnectionStatus:
    """Open the interactive Codex login flow in a separate Windows console."""
    current = get_codex_connection_status(settings)
    if not current.installed or current.authenticated:
        return current

    executable = resolve_codex_executable(settings.codex_command)
    if not executable:
        return current
    command = _codex_process_args(executable, ["login"])
    workspace = _create_codex_login_workspace(settings.project_root)
    try:
        process = subprocess.Popen(
            command,
            cwd=workspace,
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
    except OSError as error:
        shutil.rmtree(workspace, ignore_errors=True)
        raise RuntimeError(f"Не удалось запустить вход в Codex: {error}") from error
    except Exception:
        shutil.rmtree(workspace, ignore_errors=True)
        raise
    _schedule_codex_workspace_cleanup(process, workspace)
    return CodexConnectionStatus(
        True,
        False,
        "Окно входа открыто. Завершите авторизацию — статус обновится автоматически.",
    )


def _decode_process_output(output: bytes | None) -> str:
    if not output:
        return ""
    try:
        return output.decode("utf-8")
    except UnicodeDecodeError:
        return output.decode("cp866", errors="replace")
