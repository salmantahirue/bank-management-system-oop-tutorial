from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    """
    Immutable transaction record (audit log).

    Why immutable?
    - In real systems, transactions should not be edited after creation.
    """

    transaction_id: str
    account_id: str
    type: str  # "DEPOSIT" or "WITHDRAW"
    amount: int
    timestamp: str
    note: str = ""

    @staticmethod
    def now_iso() -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

