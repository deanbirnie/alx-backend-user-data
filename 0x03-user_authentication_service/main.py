#!/usr/bin/env python3
"""Integration test module"""
import requests
from app import AUTH


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Testing for user registration"""
    url = "http://0.0.0.0:5000/users"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'user created'}
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Testing for incorrect password"""
    url = "http://0.0.0.0:5000/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Testing login functionality"""
    url = "http://0.0.0.0:5000/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    if response.status_code == 401:
        return "Unable to login"
    assert response.status_code == 200
    response_json = response.json()
    assert "email" in response_json
    assert "message" in response_json
    assert response_json["email"] == email
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Testing profile when not logged in"""
    url = "http://0.0.0.0:5000/profile"

    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Testing profile while logged in"""
    url = "http://0.0.0.0:5000/profile"
    cookie = {
        "session_id": session_id
    }
    response = requests.get(url, cookie=cookie)
    assert response.status_code == 200
    payload = response.json()
    assert "email" in payload

    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == payload["email"]


def log_out(session_id: str) -> None:
    """Testing log out functionality"""
    url = "http://0.0.0.0:5000/sessions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "session_id": session_id
    }
    response = requests.delete(url, headers=headers, cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Testing password reset token geeration"""
    url = "http://0.0.0.0:5000/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Testing update password functionality"""
    url = "http://0.0.0.0:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Your password has been updated"
    assert response.json()["email"] == email


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
