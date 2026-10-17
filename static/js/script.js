const ratingButtons = document.querySelectorAll(".rating-option");
const feedback = document.getElementById("rating-feedback");

ratingButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        // Prevent repeated clicks while saving
        ratingButtons.forEach((item) => {
            item.disabled = true;
        });

        feedback.textContent = "Saving your feedback...";

        try {
            const response = await fetch("/api/ratings", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    rating: button.dataset.rating,
                }),
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.detail || "Could not save your feedback."
                );
            }

            ratingButtons.forEach((item) => {
                item.setAttribute(
                    "aria-pressed",
                    String(item === button)
                );
            });

            feedback.textContent =
                button.dataset.rating === "up"
                    ? "Thank you for your feedback!"
                    : "Thank you. I'll keep improving!";
        } catch (error) {
            feedback.textContent =
                "Couldn't save your rating. Please try again.";
            console.error(error);
        } finally {
            ratingButtons.forEach((item) => {
                item.disabled = false;
            });
        }
    });
});

