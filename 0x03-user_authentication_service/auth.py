#!/usr/bin/env python3
""" """
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
