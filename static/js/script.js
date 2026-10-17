const ratingButtons = document.querySelectorAll(".rating-option");
const feedback = document.getElementById("rating-feedback");

ratingButtons.forEach((button) => {
    button.addEventListener("click", () => {
        ratingButtons.forEach((item) => {
            item.setAttribute("aria-pressed", "false");
        });

        button.setAttribute("aria-pressed", "true");

        feedback.textContent =
            button.dataset.rating === "up"
                ? "Thank you for your feedback!"
                : "Thank you. I'll keep improving!";
    });
});