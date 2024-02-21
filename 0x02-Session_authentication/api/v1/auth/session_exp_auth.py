#!/usr/bin/env python3
"""
Route module for Basic Auth
"""
import base64
from os import getenv
from typing import Tuple, TypeVar
from uuid import uuid4

from models.user import User

from .session_auth import SessionAuth
from datetime


class SessionExpAuth(SessionAuth):
    """Session authentication implementation"""

    def __init__(self) -> None:
        # super().__init__()
        ind = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(ind)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {}
        session_dict = {
            "user_id": user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the session id for a given session"""

        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """retrieve current user information"""
        if request is None:
            return None
        val = self.session_cookie(request)

        if val is not None:
            id = self.user_id_for_session_id(val)
            user = User.get(id)

            return user

    def destroy_session(self, request=None):
        """delete a session from the database"""
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_obj = self.user_id_for_session_id(session_cookie)
        if user_obj is None:
            return False

        self.user_id_by_session_id.pop(session_cookie)
        return True
