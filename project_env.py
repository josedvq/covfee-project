from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_project_env(env_file: Path = ENV_FILE) -> None:
    """Load `.env` values into the process environment."""
    if not env_file.exists():
        return

    for raw_line in env_file.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


def get_env_str(name: str, default: str) -> str:
    """Return a string environment variable."""
    return os.getenv(name, default)


def get_env_int(name: str, default: int) -> int:
    """Return an integer environment variable."""
    value = os.getenv(name)
    return default if value is None or value == "" else int(value)


def get_env_bool(name: str, default: bool) -> bool:
    """Return a boolean environment variable."""
    value = os.getenv(name)
    if value is None or value == "":
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for {name}: {value}")


def get_env_optional(name: str) -> Optional[str]:
    """Return an optional environment variable."""
    value = os.getenv(name)
    return value if value else None


def get_env_path(name: str) -> Optional[str]:
    """Return an optional path environment variable."""
    value = get_env_optional(name)
    if value is None:
        return None

    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return str(path.resolve())


load_project_env()
