from __future__ import annotations

from backend.domain.account import Account
from backend.domain.exceptions import InsufficientFundsError


class CurrentAccount(Account):
    """
    Current account rules (simple version):
    - Allows overdraft up to a fixed limit.

    This demonstrates polymorphism:
    - withdraw() behaves differently from SavingsAccount.withdraw().
    """

    OVERDRAFT_LIMIT = 500  # can go down to -500

    @property
    def account_type(self) -> str:
        return "current"

    def withdraw(self, amount: int) -> int:
        self._require_positive_amount(amount)

        # Current: allow balance to go negative up to -OVERDRAFT_LIMIT.
        new_balance = self._balance - amount
        if new_balance < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(
                f"Overdraft limit exceeded. You can go down to {-self.OVERDRAFT_LIMIT}."
            )

        self._balance = new_balance
        return self._balance

