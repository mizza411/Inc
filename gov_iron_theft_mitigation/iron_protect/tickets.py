"""Ticket state machine for reports and sensor alerts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal

from .auth_roles import AuthService, User
from .store import JsonStore

TicketKind = Literal["public_report", "sensor_alert", "device_offline"]
TicketState = Literal[
    "new",
    "acknowledged",
    "assigned",
    "secured",
    "replaced",
    "false_alarm",
    "closed",
]

# Allowed forward transitions (plus closed from terminal outcomes).
TRANSITIONS: dict[TicketState, frozenset[TicketState]] = {
    "new": frozenset({"acknowledged", "false_alarm", "closed"}),
    "acknowledged": frozenset({"assigned", "false_alarm", "closed"}),
    "assigned": frozenset({"secured", "replaced", "false_alarm", "closed"}),
    "secured": frozenset({"closed", "replaced"}),
    "replaced": frozenset({"closed"}),
    "false_alarm": frozenset({"closed"}),
    "closed": frozenset(),
}


@dataclass
class Ticket:
    ticket_id: str
    kind: TicketKind
    state: TicketState
    created_at: str
    asset_id: str | None = None
    text: str = ""
    assignee: str | None = None
    acknowledged_at: str | None = None
    confirmed_missing_at: str | None = None
    secured_at: str | None = None
    closed_at: str | None = None
    outcome_photo_ref: str = ""
    audit: list[dict] = field(default_factory=list)

    def to_row(self) -> dict:
        return asdict(self)


class TicketService:
    def __init__(self, store: JsonStore, auth: AuthService) -> None:
        self.store = store
        self.auth = auth

    def list(self, state: TicketState | None = None) -> list[Ticket]:
        tickets = [self._from_row(r) for r in self.store.section("tickets")]
        if state:
            tickets = [t for t in tickets if t.state == state]
        return tickets

    def get(self, ticket_id: str) -> Ticket:
        for t in self.list():
            if t.ticket_id == ticket_id:
                return t
        raise KeyError(ticket_id)

    def create(
        self,
        ticket_id: str,
        kind: TicketKind,
        *,
        asset_id: str | None = None,
        text: str = "",
        confirmed_missing: bool = False,
    ) -> Ticket:
        if any(t.ticket_id == ticket_id for t in self.list()):
            raise ValueError(f"ticket exists: {ticket_id}")
        now = _utc_now()
        ticket = Ticket(
            ticket_id=ticket_id,
            kind=kind,
            state="new",
            created_at=now,
            asset_id=asset_id,
            text=text,
            confirmed_missing_at=now if confirmed_missing else None,
            audit=[{"at": now, "event": "created", "by": "system"}],
        )
        rows = self.store.section("tickets")
        rows.append(ticket.to_row())
        self.store.replace_section("tickets", rows)
        return ticket

    def transition(
        self,
        ticket_id: str,
        new_state: TicketState,
        actor_user_id: str,
        *,
        assignee: str | None = None,
        outcome_photo_ref: str = "",
    ) -> Ticket:
        user = self.auth.get(actor_user_id)
        if not user.active:
            raise PermissionError("user inactive")
        if not user.can_edit_tickets():
            raise PermissionError("role cannot edit tickets")

        rows = self.store.section("tickets")
        for row in rows:
            if row["ticket_id"] != ticket_id:
                continue
            ticket = self._from_row(row)
            allowed = TRANSITIONS[ticket.state]
            if new_state not in allowed:
                raise ValueError(
                    f"cannot move {ticket.state} -> {new_state}"
                )
            now = _utc_now()
            ticket.state = new_state
            ticket.audit.append(
                {
                    "at": now,
                    "event": f"state:{new_state}",
                    "by": actor_user_id,
                }
            )
            if new_state == "acknowledged":
                ticket.acknowledged_at = now
            if new_state == "assigned":
                ticket.assignee = assignee or actor_user_id
            if new_state in {"secured", "replaced"}:
                ticket.secured_at = now
                if outcome_photo_ref:
                    ticket.outcome_photo_ref = outcome_photo_ref
                if ticket.confirmed_missing_at is None:
                    ticket.confirmed_missing_at = ticket.created_at
            if new_state == "closed":
                ticket.closed_at = now
            # write back
            idx = rows.index(row)
            rows[idx] = ticket.to_row()
            self.store.replace_section("tickets", rows)
            return ticket
        raise KeyError(ticket_id)

    @staticmethod
    def _from_row(row: dict) -> Ticket:
        return Ticket(
            ticket_id=row["ticket_id"],
            kind=row["kind"],
            state=row["state"],
            created_at=row["created_at"],
            asset_id=row.get("asset_id"),
            text=row.get("text", ""),
            assignee=row.get("assignee"),
            acknowledged_at=row.get("acknowledged_at"),
            confirmed_missing_at=row.get("confirmed_missing_at"),
            secured_at=row.get("secured_at"),
            closed_at=row.get("closed_at"),
            outcome_photo_ref=row.get("outcome_photo_ref", ""),
            audit=list(row.get("audit") or []),
        )


def require_editor(user: User) -> None:
    if not user.can_edit_tickets():
        raise PermissionError("read-only role")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
