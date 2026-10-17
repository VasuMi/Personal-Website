
from app.database import get_connection


def create_blog_posts_table():
    query = """
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_published BOOLEAN NOT NULL DEFAULT FALSE
    );
    """

    with get_connection() as conn:
        conn.execute(query)


def create_admin_users_table():
    query = """
    CREATE TABLE IF NOT EXISTS admin_users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    with get_connection() as conn:
        conn.execute(query)


def create_ratings_table():
    query = """
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        rating VARCHAR(10) NOT NULL
            CHECK (rating IN ('up', 'down')),
        created_at TIMESTAMPTZ NOT NULL
            DEFAULT CURRENT_TIMESTAMP
    );
    """

    with get_connection() as conn:
        conn.execute(query)
