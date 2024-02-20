#!/usr/bin/env python3
"""0x03. User authentication service"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model class"""

    """Attributes:
        __tablename__ (str): The name of the table in the database where
        user records are stored.
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID of the user, used to maintain
        user sessions.
        reset_token (str): The reset token of the user, used for password
        resets.
    """
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(128), nullable=False)
    hashed_password = Column("hashed_password", String(128), nullable=False)
    session_id = Column("session_id", String(128), nullable=True)
    reset_token = Column("reset_token", String(128), nullable=True)
