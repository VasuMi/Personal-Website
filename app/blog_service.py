
from app.database import get_connection


def get_published_posts():
    query = """
        SELECT id, title, content, created_at
        FROM blog_posts
        WHERE is_published = TRUE
        ORDER BY created_at DESC;
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3].isoformat(),
        }
        for row in rows
    ]

def get_published_post(post_id: int):
    query = """
        SELECT id, title, content, created_at
        FROM blog_posts
        WHERE id = %s AND is_published = TRUE;
    """

    with get_connection() as conn:
        row = conn.execute(query, (post_id,)).fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "created_at": row[3].isoformat(),
    }


def create_blog_post(title: str, content: str, is_published: bool = False):
    query = """
        INSERT INTO blog_posts (title, content, is_published)
        VALUES (%s, %s, %s)
        RETURNING id, title, content, created_at, is_published;
    """

    with get_connection() as conn:
        row = conn.execute(
            query,
            (title, content, is_published)
        ).fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "created_at": row[3].isoformat(),
        "is_published": row[4],
    }


def update_blog_post(
    post_id: int,
    title: str,
    content: str,
    is_published: bool,
):
    query = """
        UPDATE blog_posts
        SET title = %s,
            content = %s,
            is_published = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, title, content, created_at, updated_at, is_published;
    """

    with get_connection() as conn:
        row = conn.execute(
            query,
            (title, content, is_published, post_id),
        ).fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "created_at": row[3].isoformat(),
        "updated_at": row[4].isoformat(),
        "is_published": row[5],
    }


def delete_blog_post(post_id: int):
    query = """
        DELETE FROM blog_posts
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as conn:
        row = conn.execute(
            query,
            (post_id,),
        ).fetchone()

    return row is not None


def get_all_blog_posts():
    query = """
        SELECT id, title, content, created_at, is_published
        FROM blog_posts
        ORDER BY created_at DESC;
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3].isoformat(),
            "is_published": row[4],
        }
        for row in rows
    ]


from app.database import get_connection


def save_rating(rating: str):
    query = """
        INSERT INTO ratings (rating)
        VALUES (%s)
        RETURNING id, rating, created_at;
    """

    with get_connection() as conn:
        row = conn.execute(query, (rating,)).fetchone()

    return {
        "id": row[0],
        "rating": row[1],
        "created_at": row[2].isoformat(),
    }
