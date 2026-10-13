"""Named users and roles for pilot ops."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from .store import JsonStore

Role = Literal["works_dispatcher", "works_crew", "ict_admin", "liaison_readonly", "vendor_admin"]

VALID_ROLES: frozenset[str] = frozenset(
    {
        "works_dispatcher",
        "works_crew",
        "ict_admin",
        "liaison_readonly",
        "vendor_admin",
    }
)


@dataclass
class User:
    user_id: str
    display_name: str
    role: Role
    active: bool = True

    def can_edit_tickets(self) -> bool:
        return self.role in {
            "works_dispatcher",
            "works_crew",
            "ict_admin",
            "vendor_admin",
        }

    def can_manage_users(self) -> bool:
        return self.role in {"ict_admin", "vendor_admin"}


class AuthService:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def list_users(self) -> list[User]:
        return [self._from_row(r) for r in self.store.section("users")]

    def add_user(self, user_id: str, display_name: str, role: Role) -> User:
        if role not in VALID_ROLES:
            raise ValueError(f"invalid role: {role}")
        if any(u.user_id == user_id for u in self.list_users()):
            raise ValueError(f"user exists: {user_id}")
        user = User(user_id=user_id, display_name=display_name, role=role)
        rows = self.store.section("users")
        rows.append(asdict(user))
        self.store.replace_section("users", rows)
        return user

    def disable_user(self, user_id: str) -> User:
        rows = self.store.section("users")
        for row in rows:
            if row["user_id"] == user_id:
                row["active"] = False
                self.store.replace_section("users", rows)
                return self._from_row(row)
        raise KeyError(user_id)

    def get(self, user_id: str) -> User:
        for u in self.list_users():
            if u.user_id == user_id:
                return u
        raise KeyError(user_id)

    @staticmethod
    def _from_row(row: dict) -> User:
        return User(
            user_id=row["user_id"],
            display_name=row["display_name"],
            role=row["role"],
            active=bool(row.get("active", True)),
        )
