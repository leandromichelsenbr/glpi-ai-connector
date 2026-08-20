from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "sim"}


def _ids(name: str) -> set[int]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return set()
    return {int(x.strip()) for x in raw.split(",") if x.strip()}


@dataclass(frozen=True, slots=True)
class Settings:
    glpi_url: str
    app_token: str
    user_token: str
    timeout: float = 30.0
    allowed_entity_ids: set[int] = frozenset()
    allow_create: bool = True
    allow_update: bool = True
    allow_followup: bool = True
    allow_assignment: bool = True
    allow_status_change: bool = True
    allow_solution: bool = True
    allow_close: bool = False
    audit_file: str | None = "logs/audit.jsonl"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            glpi_url=os.environ["GLPI_URL"].rstrip("/"),
            app_token=os.environ["GLPI_APP_TOKEN"],
            user_token=os.environ["GLPI_USER_TOKEN"],
            timeout=float(os.getenv("GLPI_TIMEOUT", "30")),
            allowed_entity_ids=_ids("GLPI_ALLOWED_ENTITY_IDS"),
            allow_create=_bool("GLPI_ALLOW_CREATE", True),
            allow_update=_bool("GLPI_ALLOW_UPDATE", True),
            allow_followup=_bool("GLPI_ALLOW_FOLLOWUP", True),
            allow_assignment=_bool("GLPI_ALLOW_ASSIGNMENT", True),
            allow_status_change=_bool("GLPI_ALLOW_STATUS_CHANGE", True),
            allow_solution=_bool("GLPI_ALLOW_SOLUTION", True),
            allow_close=_bool("GLPI_ALLOW_CLOSE", False),
            audit_file=os.getenv("GLPI_AUDIT_FILE", "logs/audit.jsonl") or None,
        )
