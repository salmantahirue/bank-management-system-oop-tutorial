from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """
    A simple domain model for a bank user/customer.

    We keep it "mostly data":
    - Authentication rules belong in AuthService (service layer).
    - Storage belongs in repositories (storage layer).
    """

    user_id: str
    username: str
    password_hash: str
    created_at: str

    @staticmethod
    def now_iso() -> str:
        """Return current UTC timestamp as an ISO string (easy to store in JSON)."""
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

