# business/UserManager.py

from models import User
from typing import List

class UserManager:
    def __init__(self, users: List[User]):
        self.users = users
        self.admin_email = 'admin@hotel.com'
        self.admin_password = 'admin123'  # Festgelegtes Admin-Passwort

    def register_user(self, email: str, password: str) -> User:
        user_id = max(user.user_id for user in self.users) + 1 if self.users else 1
        new_user = User(user_id, email, password, [])
        self.users.append(new_user)
        return new_user

    def login_user(self, email: str, password: str) -> User:
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None

    def is_admin(self, email: str, password: str) -> bool:
        return email == self.admin_email and password == self.admin_password
