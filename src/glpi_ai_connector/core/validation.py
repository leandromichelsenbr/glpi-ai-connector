from __future__ import annotations


VALID_URGENCIES = {1, 2, 3, 4, 5, 6}
VALID_TICKET_TYPES = {1, 2}
VALID_TICKET_STATUSES = {1, 2, 3, 4, 5, 6}


def validate_ticket_id(ticket_id: int) -> None:
    if ticket_id <= 0:
        raise ValueError("ticket_id deve ser maior que zero.")


def validate_user_id(user_id: int) -> None:
    if user_id <= 0:
        raise ValueError("user_id deve ser maior que zero.")


def validate_urgency(urgency: int) -> None:
    if urgency not in VALID_URGENCIES:
        raise ValueError("urgency deve estar entre 1 e 6.")


def validate_ticket_type(ticket_type: int) -> None:
    if ticket_type not in VALID_TICKET_TYPES:
        raise ValueError("ticket_type deve ser 1 (incidente) ou 2 (requisição).")


def validate_status(status: int) -> None:
    if status not in VALID_TICKET_STATUSES:
        raise ValueError("status deve estar entre 1 e 6.")


def validate_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} não pode ser vazio.")
