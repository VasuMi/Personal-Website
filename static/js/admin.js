
const postList = document.getElementById("admin-post-list");
const blogForm = document.getElementById("blog-form");
const titleInput = document.getElementById("post-title");
const contentInput = document.getElementById("post-content");
const publishedInput = document.getElementById("post-published");
const feedback = document.getElementById("admin-feedback");
const formHeading = document.getElementById("form-heading");
const saveButton = document.getElementById("save-post");
const cancelButton = document.getElementById("cancel-edit");

let editingPostId = null;


// Load all posts from the backend
async function loadPosts() {
    postList.textContent = "Loading posts...";

    try {
        const response = await fetch("/api/admin/blog");

        if (!response.ok) {
            throw new Error("Could not load posts.");
        }

        const posts = await response.json();
        postList.replaceChildren();

        if (posts.length === 0) {
            postList.textContent = "No posts yet. Write your first one!";
            return;
        }

        posts.forEach((post) => {
            const article = document.createElement("article");
            article.className = "admin-post-item";

            const title = document.createElement("h3");
            title.textContent = post.title;

            const status = document.createElement("p");
            status.textContent = post.is_published
                ? "Published"
                : "Draft";

            const date = document.createElement("p");
            date.textContent = post.created_at.slice(0, 10);

            const editButton = document.createElement("button");
            editButton.type = "button";
            editButton.textContent = "Edit";

            editButton.addEventListener("click", () => {
                editingPostId = post.id;

                titleInput.value = post.title;
                contentInput.value = post.content;
                publishedInput.checked = post.is_published;

                formHeading.textContent = "Edit post";
                saveButton.textContent = "Update post";
                cancelButton.hidden = false;
                feedback.textContent = "";

                blogForm.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });

                titleInput.focus();
            });

            
const deleteButton = document.createElement("button");
deleteButton.type = "button";
deleteButton.textContent = "Delete";

deleteButton.addEventListener("click", async () => {
    const confirmed = window.confirm(
        `Are you sure you want to delete "${post.title}"?`
    );

    if (!confirmed) {
        return;
    }

    deleteButton.disabled = true;

    try {
        const response = await fetch(`/api/blog/${post.id}`, {
            method: "DELETE",
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Could not delete the post."
            );
        }

        if (editingPostId === post.id) {
            resetEditor();
        }

        feedback.textContent = "Post deleted successfully!";
        await loadPosts();

    } catch (error) {
        feedback.textContent = error.message;
        deleteButton.disabled = false;
    }
});

article.append(title, status, date, editButton, deleteButton);
postList.appendChild(article);

        });

    } catch (error) {
        postList.textContent = error.message;
    }
}


// Create a new post or update an existing one
blogForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const postData = {
        title: titleInput.value.trim(),
        content: contentInput.value.trim(),
        is_published: publishedInput.checked,
    };

    if (!postData.title || !postData.content) {
        feedback.textContent = "Please enter both a title and content.";
        return;
    }

    const isEditing = editingPostId !== null;

    const url = isEditing
        ? `/api/blog/${editingPostId}`
        : "/api/blog";

    const method = isEditing ? "PUT" : "POST";

    saveButton.disabled = true;

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(postData),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not save the post.");
        }

        feedback.textContent = isEditing
            ? "Post updated successfully!"
            : "Post created successfully!";

        resetEditor();
        await loadPosts();

    } catch (error) {
        feedback.textContent = error.message;
    } finally {
        saveButton.disabled = false;
    }
});


// Return the editor to new-post mode
function resetEditor() {
    editingPostId = null;
    blogForm.reset();

    formHeading.textContent = "Write a new post";
    saveButton.textContent = "Save post";
    cancelButton.hidden = true;
}


// Cancel editing
cancelButton.addEventListener("click", () => {
    resetEditor();
    feedback.textContent = "Editing cancelled.";
});


// Initial page load
loadPosts();


const logoutButton = document.getElementById("logout-button");

logoutButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/logout", {
            method: "POST",
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error("Could not log out.");
        }

        window.location.href = "/login";
    } catch (error) {
        feedback.textContent = error.message;
    }
});