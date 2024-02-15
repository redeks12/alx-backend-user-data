#!/usr/bin/env python3
"""
Route module for Auth
"""
from typing import List, TypeVar
from os import getenv


class Auth:
    """auth class for authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication
        return
            - False"""

        if not excluded_paths or not path:
            return True
        if path.endswith("/") or path.endswith("*"):
            path = path[:-1]
        for idx, ex in enumerate(excluded_paths):
            if ex.endswith("/") or path.endswith("*"):
                excluded_paths[idx] = ex[:-1]

        for pth in excluded_paths:
            if pth in path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """require authorization header
        - return False"""
        if request is None:
            return None

        val = request.headers.get("Authorization", None)
        if val:
            return val
        else:
            return None

    def current_user(self, request=None) -> TypeVar("User"):
        """get current user
        - return None"""
        return None

    def session_cookie(self, request=None):
        """get session cookie from request"""
        if request is None:
            return None
        cookie_name = getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
