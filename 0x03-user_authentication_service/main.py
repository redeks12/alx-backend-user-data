# !/usr/bin/env python3
"""0x03. User authentication service"""
import requests

URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register new user"""
    req = requests.post(f"{URL}/users", data={"email": email, "password": password})
    req.raise_for_status()
    assert req.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    req = requests.post(f"{URL}/sessions", data={"email": email, "password": password})
    assert req.status_code == 401


def log_in(email: str, password: str) -> str:
    """login with email and password"""
    req = requests.post(f"{URL}/sessions", data={"email": email, "password": password})
    assert req.status_code == 200
    return req.cookies.get("session_id")


def profile_unlogged() -> None:
    """login with email and password"""
    req = requests.get(f"{URL}/profile")
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    """login with email and password"""
    req = requests.get(f"{URL}/profile", cookies={"session_id": session_id})
    assert req.status_code == 200


def log_out(session_id: str) -> None:
    """login with email and password"""
    req = requests.delete(f"{URL}/sessions", cookies={"session_id": session_id})

    assert req.status_code == 302


def reset_password_token(email: str) -> str:
    """reset password token"""
    req = requests.post(f"{URL}/reset_password", data={"email": email})
    assert req.status_code == 200
    data = req.json()
    return data.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password for user"""
    req = requests.put(
        f"{URL}/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert req.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
