
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from app.blog_service import create_blog_post

from fastapi import HTTPException
from fastapi import Depends

from app.blog_service import get_published_posts

from app.blog_service import update_blog_post

from app.blog_service import delete_blog_post

from app.blog_service import get_all_blog_posts


from fastapi import Response
from app.auth import verify_admin, create_access_token
from app.auth import require_admin


app = FastAPI(title="VasuMi")

# Serve CSS, JavaScript, and images
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Load HTML templates
templates = Jinja2Templates(directory="templates")

#--------------------------------------

class BlogPostInput(BaseModel):
    title: str
    content: str
    is_published: bool = False


class LoginInput(BaseModel):
    username: str
    password: str


@app.post("/api/blog")
def add_blog_post(post: BlogPostInput):
    return create_blog_post(
        title=post.title,
        content=post.content,
        is_published=post.is_published,
    )

#------------------------------------------


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# @app.get("/projects")
# def projects(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="projects.html",
#         context={}
#     )

@app.get("/blog")
def blog(request: Request):
    posts = get_published_posts()

    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={"posts": posts}
    )



@app.get("/blog")
def blog(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={}
    )

# @app.get("/blog/post")
# def blog_post(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="post.html",
#         context={}
#     )
from app.blog_service import get_published_post

@app.get("/blog/{post_id}")
def blog_post(request: Request, post_id: int):
    post = get_published_post(post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Blog post not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post}
    )


@app.get("/postbox")
def postbox(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="postbox.html",
        context={}
    )

@app.get("/api/blog")
def list_blog_posts():
    admin: dict = Depends(require_admin)
    return get_published_posts()


@app.put("/api/blog/{post_id}")
def edit_blog_post(post_id: int, post: BlogPostInput):
    admin: dict = Depends(require_admin)
    updated_post = update_blog_post(
        post_id=post_id,
        title=post.title,
        content=post.content,
        is_published=post.is_published,
    )

    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail="Blog post not found",
        )

    return updated_post


@app.delete("/api/blog/{post_id}")
def remove_blog_post(post_id: int):
    admin: dict = Depends(require_admin)
    deleted = delete_blog_post(post_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Blog post not found",
        )

    return {"message": "Blog post deleted successfully"}

from app.auth import require_admin
# @app.get("/admin")
# def admin_dashboard(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="admin.html",
#         context={}
#     )

@app.get("/admin")
def admin_dashboard(
    request: Request,
    admin: dict = Depends(require_admin),
):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={},
    )



# @app.get("/api/admin/blog")
# def list_all_blog_posts():
#     return get_all_blog_posts()
@app.get("/api/admin/blog")
def list_all_blog_posts(
    admin: dict = Depends(require_admin),
):
    return get_all_blog_posts()


@app.post("/api/login")
def admin_login(data: LoginInput, response: Response):
    user = verify_admin(data.username, data.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(
        user_id=user["id"],
        username=user["username"],
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Local HTTP development only
        samesite="lax",
        max_age=7200,
        path="/",
    )

    return {"message": "Login successful"}


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )

@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}