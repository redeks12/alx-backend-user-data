#!/usr/bin/env python3
"""0x00. Personal data"""

from bcrypt import checkpw, gensalt, hashpw


def hash_password(password: str) -> bytes:
    """User passwords should NEVER be stored in plain text in a database."""
    return hashpw(password.encode(), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid function that expects 2 arguments and returns a boolean."""
    return checkpw(password.encode(), hashed_password)
