#!/usr/bin/env python3
"""
Route module for Basic Auth
"""
import base64
from typing import Tuple, TypeVar

from models.user import User

from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication implementation"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None or type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None

        try:
            val = base64.b64decode(base64_authorization_header).decode("utf-8")
            return val

        except:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
        ):
            return (None, None)

        if ":" in decoded_base64_authorization_header:
            vals = decoded_base64_authorization_header.split(":")
            lc = [vals[0], ":".join(vals[1:])]
            return tuple(lc)

        return (None, None)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        user = User.search({"email": user_email})
        if user:
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        authHead = self.authorization_header(request)
        if not authHead:
            return

        authh = self.extract_base64_authorization_header(authHead)

        if authh is None:
            return

        decoded_auth_head = self.decode_base64_authorization_header(authh)

        if decoded_auth_head is None:
            return

        extracted_user_credentials = self.extract_user_credentials(decoded_auth_head)
        print(extracted_user_credentials)
        if extracted_user_credentials[0] is None:
            return

        user = self.user_object_from_credentials(
            extracted_user_credentials[0], extracted_user_credentials[1]
        )

        return user
