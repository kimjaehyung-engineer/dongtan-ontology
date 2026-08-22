from dataclasses import dataclass
from collections.abc import Mapping
import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "00_원본_데이터"
REPORT_DIR = PROJECT_ROOT / "03_보고서_및_출력"


class ConfigurationError(RuntimeError):
    """Raised when runtime configuration is missing or inconsistent."""


@dataclass(frozen=True)
class DatabaseConfig:
    uri: str
    username: str = ""
    password: str = ""

    @property
    def auth(self) -> tuple[str, str] | None:
        if not self.username and not self.password:
            return None
        return self.username, self.password

    def driver_kwargs(self) -> dict[str, object]:
        if self.auth is None:
            return {}
        return {"auth": self.auth}


@dataclass(frozen=True)
class ProjectPaths:
    nodes_csv: Path
    relationships_csv: Path
    ontology_output: Path


def _environment(values: Mapping[str, str] | None) -> Mapping[str, str]:
    return os.environ if values is None else values


def _validate_credential_pair(
    username: str,
    password: str,
    username_key: str,
    password_key: str,
) -> None:
    if username and not password:
        raise ConfigurationError(f"Set {password_key} when {username_key} is configured.")
    if password and not username:
        raise ConfigurationError(f"Set {username_key} when {password_key} is configured.")


def load_local_database_config(
    values: Mapping[str, str] | None = None,
) -> DatabaseConfig:
    environment = _environment(values)
    username = environment.get("DONGTAN_LOCAL_USER", "")
    password = environment.get("DONGTAN_LOCAL_PASSWORD", "")
    _validate_credential_pair(
        username,
        password,
        "DONGTAN_LOCAL_USER",
        "DONGTAN_LOCAL_PASSWORD",
    )
    return DatabaseConfig(
        uri=environment.get("DONGTAN_LOCAL_URI") or "bolt://localhost:7687",
        username=username,
        password=password,
    )


def load_cloud_database_config(
    values: Mapping[str, str] | None = None,
) -> DatabaseConfig:
    environment = _environment(values)
    required_keys = (
        "DONGTAN_CLOUD_URI",
        "DONGTAN_CLOUD_USER",
        "DONGTAN_CLOUD_PASSWORD",
    )
    missing_keys = [key for key in required_keys if not environment.get(key)]
    if missing_keys:
        joined_keys = ", ".join(missing_keys)
        raise ConfigurationError(
            f"Set the required cloud environment variables: {joined_keys}."
        )

    return DatabaseConfig(
        uri=environment["DONGTAN_CLOUD_URI"],
        username=environment["DONGTAN_CLOUD_USER"],
        password=environment["DONGTAN_CLOUD_PASSWORD"],
    )


def _configured_path(value: str | None, default: Path) -> Path:
    if not value:
        return default
    configured = Path(value).expanduser()
    if configured.is_absolute():
        return configured
    return PROJECT_ROOT / configured


def load_project_paths(
    values: Mapping[str, str] | None = None,
) -> ProjectPaths:
    environment = _environment(values)
    return ProjectPaths(
        nodes_csv=_configured_path(
            environment.get("DONGTAN_NODES_CSV"),
            DATA_DIR / "rfp_nodes.csv",
        ),
        relationships_csv=_configured_path(
            environment.get("DONGTAN_RELATIONSHIPS_CSV"),
            DATA_DIR / "rfp_relationships.csv",
        ),
        ontology_output=_configured_path(
            environment.get("DONGTAN_ONTOLOGY_OUTPUT"),
            REPORT_DIR / "ontology.json",
        ),
    )


def run_python_script(
    script_directory: Path,
    script_name: str,
    *arguments: str,
) -> subprocess.CompletedProcess[bytes]:
    command = [
        sys.executable,
        str(script_directory / script_name),
        *(str(argument) for argument in arguments),
    ]
    return subprocess.run(command, check=False)
