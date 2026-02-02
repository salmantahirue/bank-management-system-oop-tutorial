from typing import Optional, List
from backend.domain.account import Account
from backend.domain.savings_account import SavingsAccount
from backend.domain.current_account import CurrentAccount
from backend.storage.json_store import JsonStore

class AccountRepository:
    """
    Handles persistence for Account objects.
    Polymorphism in action: Reconstructs the correct subclass (Savings/Current) on load.
    """

    def save(self, account: Account) -> None:
        data = JsonStore.load_data()
        
        # Remove existing version of this account
        data["accounts"] = [a for a in data["accounts"] if a["account_id"] != account.account_id]

        # Serialize
        acc_dict = {
            "account_id": account.account_id,
            "user_id": account.user_id,
            "balance": account.balance,
            "type": account.account_type  # store type so we know which class to load later
        }
        data["accounts"].append(acc_dict)
        JsonStore.save_data(data)

    def find_by_user_id(self, user_id: str) -> Optional[Account]:
        """Finds the main account for a user (simplified: 1 account per user for now)."""
        data = JsonStore.load_data()
        for a in data["accounts"]:
            if a["user_id"] == user_id:
                return self._deserialize(a)
        return None
    
    def find_by_id(self, account_id: str) -> Optional[Account]:
        data = JsonStore.load_data()
        for a in data["accounts"]:
            if a["account_id"] == account_id:
                return self._deserialize(a)
        return None

    def _deserialize(self, data: dict) -> Account:
        """Converts raw dict to SavingsAccount or CurrentAccount."""
        acc_type = data.get("type")
        
        # We access _balance via the constructor or a workaround.
        # Since our models init validation checks balance >= 0, we pass it safely.
        
        if acc_type == "savings":
            return SavingsAccount(
                account_id=data["account_id"],
                user_id=data["user_id"],
                balance=data["balance"]
            )
        elif acc_type == "current":
            return CurrentAccount(
                account_id=data["account_id"],
                user_id=data["user_id"],
                balance=data["balance"]
            )
        else:
            # Fallback or error for unknown types
            raise ValueError(f"Unknown account type: {acc_type}")
