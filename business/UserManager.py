# business/UserManager.py
import hashlib
from models import User

class UserManager:
    def __init__(self, users):
        self.users = users

    # User Story 1.6: Register user with email and password
    def register_user(self, email: str, password: str) -> User:
        if any(user.email == email for user in self.users):
            raise ValueError("Email already registered")
        user_id = len(self.users) + 1
        hashed_password = self._hash_password(password)
        new_user = User(user_id=user_id, email=email, password=hashed_password, booking_history=[])
        self.users.append(new_user)
        return new_user

    # User Story 2.1: Login user to access booking history
    def login_user(self, email: str, password: str) -> User:
        hashed_password = self._hash_password(password)
        for user in self.users:
            if user.email == email and user.password == hashed_password:
                return user
        raise ValueError("Invalid email or password")

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
