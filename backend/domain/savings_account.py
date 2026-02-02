from __future__ import annotations

from backend.domain.account import Account
from backend.domain.exceptions import InsufficientFundsError, ValidationError


class SavingsAccount(Account):
    """
    Savings account rules (simple version):
    - Cannot go below 0 (no overdraft).
    """

    def __init__(self, account_id: str, user_id: str, balance: int) -> None:
        # Savings accounts cannot have negative balance, even when loading from storage
        if balance < 0:
            raise ValidationError("Savings account balance cannot be negative.")
        super().__init__(account_id, user_id, balance)

    @property
    def account_type(self) -> str:
        return "savings"

    def withdraw(self, amount: int) -> int:
        self._require_positive_amount(amount)

        # Savings: no overdraft.
        if amount > self._balance:
            raise InsufficientFundsError("Savings account cannot go below 0.")

        self._balance -= amount
        return self._balance

