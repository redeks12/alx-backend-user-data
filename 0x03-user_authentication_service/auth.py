#!/usr/bin/env python3
"""0x03. User authentication service"""
from bcrypt import gensalt, hashpw
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password using password argument"""

    return hashpw(password.encode(), salt=gensalt())


from db import DB


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user with the given email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except:
            hashed = _hash_password(password)
            self._db.add_user(email=email, hashed_password=hashed)
        else:
            raise ValueError(f"User {user.email} already exists")
