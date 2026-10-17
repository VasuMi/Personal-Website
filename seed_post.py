
from app.database import get_connection

query = """
    INSERT INTO blog_posts (title, content, is_published)
    VALUES (%s, %s, %s);
"""

with get_connection() as conn:
    conn.execute(
        query,
        (
            "My Journey into Backend Development",
            "Today, I connected my FastAPI backend to PostgreSQL. "
            "I am learning how a website retrieves and displays data "
            "from a database.",
            True,
        ),
    )

print("Sample blog post added successfully!")
