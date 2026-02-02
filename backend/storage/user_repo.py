from typing import Optional, List
from backend.domain.user import User
from backend.storage.json_store import JsonStore

class UserRepository:
    """
    Handles persistence for User objects.
    """

    def save(self, user: User) -> None:
        data = JsonStore.load_data()
        # Remove existing if update, or just append
        # For simplicity in this learning project, we'll check by ID
        data["users"] = [u for u in data["users"] if u["user_id"] != user.user_id]
        
        # Serialize
        user_dict = {
            "user_id": user.user_id,
            "username": user.username,
            "password_hash": user.password_hash,
            "created_at": user.created_at
        }
        data["users"].append(user_dict)
        JsonStore.save_data(data)

    def find_by_username(self, username: str) -> Optional[User]:
        data = JsonStore.load_data()
        for u in data["users"]:
            if u["username"] == username:
                return User(
                    user_id=u["user_id"],
                    username=u["username"],
                    password_hash=u["password_hash"],
                    created_at=u["created_at"]
                )
        return None

    def find_by_id(self, user_id: str) -> Optional[User]:
        data = JsonStore.load_data()
        for u in data["users"]:
            if u["user_id"] == user_id:
                return User(**u)
        return None
