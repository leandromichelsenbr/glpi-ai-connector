from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AuditEvent:
    timestamp: str
    operation: str
    target_type: str
    target_id: int | None
    success: bool
    details: dict[str, Any]


class AuditLogger:
    def __init__(self, path: str | None = None) -> None:
        self.path = Path(path) if path else None

    def record(
        self,
        operation: str,
        *,
        target_type: str = "Ticket",
        target_id: int | None = None,
        success: bool = True,
        details: dict[str, Any] | None = None,
    ) -> None:
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            success=success,
            details=details or {},
        )
        payload = asdict(event)
        logger.info("AUDIT %s", json.dumps(payload, ensure_ascii=False))

        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
