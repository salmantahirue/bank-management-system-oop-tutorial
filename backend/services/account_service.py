import uuid
from typing import List, Dict, Any
from backend.domain.transaction import Transaction
from backend.domain.exceptions import NotFoundError, ValidationError
from backend.storage.account_repo import AccountRepository
from backend.storage.transaction_repo import TransactionRepository
from backend.storage.user_repo import UserRepository

class AccountService:
    def __init__(self):
        self.account_repo = AccountRepository()
        self.transaction_repo = TransactionRepository()
        self.user_repo = UserRepository()

    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        """Returns user info + account info for the dashboard."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
            
        account = self.account_repo.find_by_user_id(user_id)
        if not account:
            # Should not happen if registered correctly
            raise NotFoundError("No account found for this user.")
            
        return {
            "username": user.username,
            "account_id": account.account_id,
            "account_type": account.account_type,
            "balance": account.balance
        }

    def deposit(self, user_id: str, amount: int) -> int:
        account = self._get_account(user_id)
        
        # Domain logic: account.deposit()
        new_balance = account.deposit(amount)
        
        # Persist change
        self.account_repo.save(account)
        
        # Record transaction
        self._log_transaction(account.account_id, "DEPOSIT", amount)
        
        return new_balance

    def withdraw(self, user_id: str, amount: int) -> int:
        account = self._get_account(user_id)
        
        # Domain logic: account.withdraw() (Polymorphic!)
        new_balance = account.withdraw(amount)
        
        # Persist change
        self.account_repo.save(account)
        
        # Record transaction
        self._log_transaction(account.account_id, "WITHDRAW", amount)
        
        return new_balance

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        account = self._get_account(user_id)
        txs = self.transaction_repo.find_by_account_id(account.account_id)
        
        # Convert to dicts for API
        return [
            {
                "timestamp": t.timestamp,
                "type": t.type,
                "amount": t.amount,
                "note": t.note
            }
            for t in txs
        ]

    def _get_account(self, user_id: str):
        account = self.account_repo.find_by_user_id(user_id)
        if not account:
            raise NotFoundError("Account not found.")
        return account

    def _log_transaction(self, account_id: str, tx_type: str, amount: int, note: str = ""):
        tx = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=account_id,
            type=tx_type,
            amount=amount,
            timestamp=Transaction.now_iso(),
            note=note
        )
        self.transaction_repo.save(tx)
