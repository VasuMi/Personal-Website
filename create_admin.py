
from getpass import getpass

from pwdlib import PasswordHash

from app.database import get_connection


password_hash = PasswordHash.recommended()

username = input("Choose your admin username: ").strip()

if not username:
    print("Username cannot be empty.")
    raise SystemExit(1)

password = getpass("Choose your admin password: ")
confirm_password = getpass("Confirm your password: ")

if len(password) < 12:
    print("Use a password with at least 12 characters.")
    raise SystemExit(1)

if password != confirm_password:
    print("Passwords do not match.")
    raise SystemExit(1)

hashed_password = password_hash.hash(password)

try:
    with get_connection() as conn:
        existing_user = conn.execute(
            "SELECT id FROM admin_users WHERE username = %s",
            (username,),
        ).fetchone()

        if existing_user:
            print("That username already exists. Choose another.")
            raise SystemExit(1)

        conn.execute(
            """
            INSERT INTO admin_users (username, password_hash)
            VALUES (%s, %s);
            """,
            (username, hashed_password),
        )

    print("Admin account created successfully!")

except Exception as error:
    print(f"Could not create admin account: {error}")
