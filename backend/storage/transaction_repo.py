from typing import List
from backend.domain.transaction import Transaction
from backend.storage.json_store import JsonStore

class TransactionRepository:
    """
    Handles persistence for Transaction objects.
    """

    def save(self, tx: Transaction) -> None:
        data = JsonStore.load_data()

        tx_dict = {
            "transaction_id": tx.transaction_id,
            "account_id": tx.account_id,
            "type": tx.type,
            "amount": tx.amount,
            "timestamp": tx.timestamp,
            "note": tx.note
        }
        data["transactions"].append(tx_dict)
        JsonStore.save_data(data)

    def find_by_account_id(self, account_id: str) -> List[Transaction]:
        data = JsonStore.load_data()
        results = []
        for t in data["transactions"]:
            if t["account_id"] == account_id:
                results.append(Transaction(**t))
        # Sort by latest first
        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results
