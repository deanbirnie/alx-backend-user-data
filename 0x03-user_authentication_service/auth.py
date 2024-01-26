#!/usr/bin/env python3
""" """
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    returns byte value of hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
