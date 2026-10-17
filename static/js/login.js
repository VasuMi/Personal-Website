
const loginForm = document.getElementById("login-form");
const feedback = document.getElementById("login-feedback");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    feedback.textContent = "Signing in...";

    const formData = new FormData(loginForm);

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "same-origin",
            body: JSON.stringify({
                username: formData.get("username"),
                password: formData.get("password"),
            }),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Login failed.");
        }

        window.location.href = "/admin";

    } catch (error) {
        feedback.textContent = error.message;
    }
});
