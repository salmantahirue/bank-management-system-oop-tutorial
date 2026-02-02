from __future__ import annotations

from abc import ABC, abstractmethod

from backend.domain.exceptions import InsufficientFundsError, ValidationError


class Account(ABC):
    """
    Abstract Base Class (Abstraction) for all account types.

    Why ABC?
    - It enforces a contract: every account type must implement withdraw rules.

    Encapsulation:
    - Balance is stored in a "protected" attribute (_balance).
    - We update it only through deposit()/withdraw() so rules are enforced.
    """

    def __init__(self, account_id: str, user_id: str, balance: int) -> None:
        self.account_id = account_id
        self.user_id = user_id

        # Note: We allow negative balance here because CurrentAccount supports overdraft.
        # Individual account types enforce their own rules in withdraw() method.
        # SavingsAccount.withdraw() prevents negative balance.
        # CurrentAccount.withdraw() allows up to -500.
        self._balance = balance

    @property
    def balance(self) -> int:
        return self._balance

    def deposit(self, amount: int) -> int:
        """
        Shared deposit logic.
        Polymorphism note:
        - Deposit rules are the same for our simple project, so we keep it here.
        """
        if amount <= 0:
            raise ValidationError("Deposit amount must be greater than 0.")
        self._balance += amount
        return self._balance

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        """
        Polymorphic behavior:
        - SavingsAccount and CurrentAccount implement different withdrawal rules.
        """

    def _require_positive_amount(self, amount: int) -> None:
        if amount <= 0:
            raise ValidationError("Withdraw amount must be greater than 0.")

    def _require_sufficient_funds(self, amount: int) -> None:
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds.")

    @property
    @abstractmethod
    def account_type(self) -> str:
        """Human-friendly account type string (used by UI)."""

