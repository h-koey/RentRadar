import ipaddress
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen


STARTUP_TIMEOUT_SECONDS = 45


def _is_local(hostname):
    if hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def _find_ollama():
    configured_path = os.environ.get("OLLAMA_EXECUTABLE")
    if configured_path:
        executable = Path(configured_path.strip('"')).expanduser()
        if executable.is_file():
            return str(executable)
        raise RuntimeError(f"OLLAMA_EXECUTABLE does not point to a file: {executable}")

    executable = shutil.which("ollama")
    if executable:
        return executable

    candidates = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("ProgramFiles")
    if local_app_data:
        candidates.extend(
            [
                Path(local_app_data) / "Programs" / "Ollama" / "ollama.exe",
                Path(local_app_data) / "Ollama" / "ollama.exe",
            ]
        )
    if program_files:
        candidates.append(Path(program_files) / "Ollama" / "ollama.exe")

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def _ollama_is_responding(base_url):
    try:
        with urlopen(f"{base_url}/api/tags", timeout=1):
            return True
    except (OSError, URLError, TimeoutError):
        return False


def ensure_local_ollama_running():
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    parsed_url = urlsplit(base_url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
        raise RuntimeError("OLLAMA_BASE_URL must be a valid HTTP or HTTPS URL.")

    if not _is_local(parsed_url.hostname) or _ollama_is_responding(base_url):
        return
    if parsed_url.scheme != "http":
        raise RuntimeError("Ollama startup requires a local HTTP OLLAMA_BASE_URL.")

    executable = _find_ollama()
    if not executable:
        raise RuntimeError(
            "Ollama is not installed or its executable was not found. Install Ollama, "
            "or set OLLAMA_EXECUTABLE in .env to the full path of ollama.exe."
        )

    try:
        port = parsed_url.port or 11434
    except ValueError as exc:
        raise RuntimeError("OLLAMA_BASE_URL contains an invalid port.") from exc
    hostname = parsed_url.hostname
    if ":" in hostname:
        hostname = f"[{hostname}]"
    process_environment = os.environ.copy()
    process_environment["OLLAMA_HOST"] = f"{hostname}:{port}"
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        process = subprocess.Popen(
            [executable, "serve"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=process_environment,
            creationflags=creation_flags,
        )
    except OSError as exc:
        raise RuntimeError(f"Could not launch Ollama executable: {exc}") from exc

    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if _ollama_is_responding(base_url):
            print("Started local Ollama server.")
            return
        if process.poll() is not None:
            raise RuntimeError(
                f"Ollama exited during startup with code {process.returncode}."
            )
        time.sleep(0.5)

    raise RuntimeError(
        f"Ollama did not become available at {base_url} "
        f"within {STARTUP_TIMEOUT_SECONDS} seconds."
    )


def start_local_ollama_for_runserver(argv):
    if len(argv) < 2 or argv[1] != "runserver":
        return

    from dotenv import load_dotenv

    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    try:
        ensure_local_ollama_running()
    except RuntimeError as exc:
        print(f"Warning: unable to start local Ollama: {exc}", file=sys.stderr)
