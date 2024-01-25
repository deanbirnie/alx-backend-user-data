#!/usr/bin/env python3
"""
This module contains a SQLAlchemy model for user authentication.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    This class creates a user model for a database table named users.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(Integer, primary_key=True)
    reset_token = Column(String(250), nullable=False)
