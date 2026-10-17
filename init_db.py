
from app.models import (
    create_blog_posts_table,
    create_admin_users_table,
    create_ratings_table,
)

create_blog_posts_table()
create_admin_users_table()
create_ratings_table()

print("Database tables created successfully!")
