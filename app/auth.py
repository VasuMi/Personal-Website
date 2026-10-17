
import os

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

from fastapi import HTTPException, Request

from app.database import get_connection

load_dotenv()

password_hash = PasswordHash.recommended()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
    raise RuntimeError(
        "Set a strong JWT_SECRET_KEY in your .env file."
    )


def verify_admin(username: str, password: str):
    query = """
        SELECT id, username, password_hash
        FROM admin_users
        WHERE username = %s;
    """

    with get_connection() as conn:
        user = conn.execute(query, (username,)).fetchone()

    if user is None:
        return None

    if not password_hash.verify(password, user[2]):
        return None

    return {
        "id": user[0],
        "username": user[1],
    }


def create_access_token(user_id: int, username: str):
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "username": username,
        "iat": now,
        "exp": now + timedelta(hours=2),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def verify_access_token(token: str):
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        return None


def require_admin(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Please log in to access this page.",
        )

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Session expired or invalid. Please log in again.",
        )

    return payload
