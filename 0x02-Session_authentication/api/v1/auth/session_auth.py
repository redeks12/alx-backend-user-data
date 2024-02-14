#!/usr/bin/env python3
"""
Route module for Basic Auth
"""
import base64
from typing import Tuple, TypeVar

from models.user import User

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session authentication implementation"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id"""
        if user_id is None or type(user_id) is not str:
            return None

        sessId = str(uuid4())
        self.user_id_by_session_id[sessId] = user_id

        return sessId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the session id for a given session"""

        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)
