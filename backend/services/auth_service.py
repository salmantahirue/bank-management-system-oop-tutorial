import uuid
import hashlib
from typing import Tuple
from backend.domain.user import User
from backend.domain.savings_account import SavingsAccount
from backend.domain.current_account import CurrentAccount
from backend.domain.exceptions import AuthError, ValidationError
from backend.storage.user_repo import UserRepository
from backend.storage.account_repo import AccountRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.account_repo = AccountRepository()

    def register(self, username: str, password: str, account_type: str) -> User:
        """
        Creates a new user AND their initial account.
        Transactional-ish: we want both or neither (simplified here).
        """
        if len(password) < 4:
            raise ValidationError("Password must be at least 4 characters.")
        
        if self.user_repo.find_by_username(username):
            raise AuthError("Username already exists.")

        # 1. Create User
        user_id = str(uuid.uuid4())
        hashed_pw = self._hash_password(password)
        user = User(
            user_id=user_id,
            username=username,
            password_hash=hashed_pw,
            created_at=User.now_iso()
        )
        self.user_repo.save(user)

        # 2. Create Account (Factory logic here or inside Account class)
        account_id = str(uuid.uuid4())
        initial_balance = 0
        
        if account_type == "savings":
            account = SavingsAccount(account_id, user_id, initial_balance)
        elif account_type == "current":
            account = CurrentAccount(account_id, user_id, initial_balance)
        else:
            raise ValidationError("Invalid account type. Choose 'savings' or 'current'.")
            
        self.account_repo.save(account)
        
        return user

    def login(self, username: str, password: str) -> Tuple[User, str]:
        """
        Returns (User, token) if successful.
        Token is just user_id for this learning project (simple session).
        """
        user = self.user_repo.find_by_username(username)
        if not user:
            raise AuthError("Invalid username or password.")
            
        if user.password_hash != self._hash_password(password):
            raise AuthError("Invalid username or password.")
            
        # In a real app, generate a secure JWT here.
        token = user.user_id 
        return user, token

    def _hash_password(self, password: str) -> str:
        # Simple SHA256 hash (in production, use bcrypt/argon2)
        return hashlib.sha256(password.encode()).hexdigest()
