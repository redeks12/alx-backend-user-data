#!/usr/bin/env python3
"""0x03. User authentication service"""
from typing import Union
from uuid import uuid4

from bcrypt import checkpw, gensalt, hashpw
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password using password argument"""

    return hashpw(password.encode(), salt=gensalt())


def _generate_uuid() -> str:
    """generate uuid from password"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user with the given email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
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
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Create a new session"""
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, "session_id", uid)
            self._db.save()
            return uid
        except (NoResultFound, InvalidRequestError):
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get_user_from_session_ id of user"""

        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """delete a session"""

        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                if hasattr(user, "session_id"):
                    setattr(user, "session_id", None)
                    return None
        except (NoResultFound, InvalidRequestError):
            pass
