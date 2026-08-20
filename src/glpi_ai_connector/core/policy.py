from __future__ import annotations

from dataclasses import dataclass, field


class PolicyDenied(PermissionError):
    """Operação negada por política do conector."""


@dataclass(slots=True)
class SecurityPolicy:
    allowed_entity_ids: set[int] = field(default_factory=set)
    allow_create: bool = True
    allow_update: bool = True
    allow_followup: bool = True
    allow_assignment: bool = True
    allow_status_change: bool = True
    allow_solution: bool = True
    allow_close: bool = False

    def check_entity(self, entity_id: int | None) -> None:
        if entity_id is None or not self.allowed_entity_ids:
            return
        if entity_id not in self.allowed_entity_ids:
            raise PolicyDenied(f"Entidade {entity_id} não permitida pela política.")

    def require(self, operation: str) -> None:
        flags = {
            "create_ticket": self.allow_create,
            "update_ticket": self.allow_update,
            "add_followup": self.allow_followup,
            "assign_technician": self.allow_assignment,
            "set_ticket_status": self.allow_status_change,
            "add_solution": self.allow_solution,
            "close_ticket": self.allow_close,
        }
        if operation in flags and not flags[operation]:
            raise PolicyDenied(f"Operação '{operation}' não permitida pela política.")
