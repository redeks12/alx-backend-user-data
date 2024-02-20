#!/usr/bin/env python3
"""0x03. User authentication service"""
from uuid import uuid4

from bcrypt import checkpw, gensalt, hashpw
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password using password argument"""

    return hashpw(password.encode(), salt=gensalt())


def _generate_uuid() -> str:
    """generate uuid from password"""
    return str(uuid4())


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
            user = self._db.add_user(email=email, hashed_password=hashed)
            return user
        else:
            raise ValueError(f"User {user.email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """check if the email is valid"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), user.hashed_password)
        except:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session"""
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, "session_id", uid)
            self._db.save()
            return uid
        except:
            pass
