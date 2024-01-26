#!/usr/bin/env python3
"""Password hashing and authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import typing


def _hash_password(password: str) -> bytes:
    """
    returns byte value of hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Create a UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validation of user credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                pwb = password.encode('utf-8')
                pwh = user.hashed_password
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create and return session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> typing.Union[str, None]:
        """Get user from session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        if user is None:
            return None
        return user
        return None
    