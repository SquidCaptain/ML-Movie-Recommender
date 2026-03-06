const searchInput = document.getElementById("search");
const resultsDiv = document.getElementById("results");

// Search movies
searchInput.addEventListener("keyup", function () {
    const query = this.value;

    if (query.length < 2) {
        resultsDiv.innerHTML = "";
        return;
    }

    fetch(`/search/?q=${query}`)
        .then(res => res.json())
        .then(data => {
            resultsDiv.innerHTML = "";

            data.forEach(movie => {
                const div = document.createElement("div");
                div.classList.add("movie-card");

                div.innerHTML = `
                    <img src="https://image.tmdb.org/t/p/w200${movie.poster}">
                    <p>${movie.title}</p>
                    <div class="star-rating" data-movie="${movie.id}"></div>
                `;

                resultsDiv.appendChild(div);

                const starsDiv = div.querySelector(".star-rating");
                renderStars(starsDiv, movie.id);
            });
        });
});

// Render stars for a movie (from saved rating or empty)
function renderStars(container, movieId) {
    container.innerHTML = "";

    const rating = USER_RATINGS[movieId] || 0;

    for (let i = 1; i <= 5; i++) {
        const img = document.createElement("img");
        img.classList.add("star");
        img.dataset.movie = movieId;
        img.dataset.star = i;

        if (rating >= i) img.src = STAR_FULL;
        else if (rating >= i - 0.5) img.src = STAR_HALF;
        else img.src = STAR_EMPTY;

        container.appendChild(img);
    }

    attachStarEvents(container);
}

// Add hover and click events for a container of stars
function attachStarEvents(container) {
    const stars = container.querySelectorAll(".star");

    stars.forEach(star => {
        const movieId = star.dataset.movie;
        const starValue = parseInt(star.dataset.star);

        // Hover preview
        star.addEventListener("mousemove", e => {
            const rect = star.getBoundingClientRect();
            const isHalf = e.clientX - rect.left < rect.width / 2;
            const hoverRating = isHalf ? starValue - 0.5 : starValue;
            updateStars(container, hoverRating);
        });

        star.addEventListener("mouseleave", () => {
            const savedRating = USER_RATINGS[movieId] || 0;
            updateStars(container, savedRating);
        });

        // Click to rate
        star.addEventListener("click", e => {
            const rect = star.getBoundingClientRect();
            const isHalf = e.clientX - rect.left < rect.width / 2;
            const clickedRating = isHalf ? starValue - 0.5 : starValue;

            submitRating(movieId, clickedRating, container);
        });
    });
}

// Update stars visually
function updateStars(container, rating) {
    const stars = container.querySelectorAll(".star");
    stars.forEach((star, idx) => {
        const starNum = idx + 1;
        if (rating >= starNum) star.src = STAR_FULL;
        else if (rating >= starNum - 0.5) star.src = STAR_HALF;
        else star.src = STAR_EMPTY;
    });
}

// Submit rating to backend
function submitRating(movieId, rating, container) {
    fetch("/rate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken(),
        },
        body: `movie_id=${movieId}&rating=${rating}`,
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                USER_RATINGS[movieId] = rating;
                updateStars(container, rating);
            }
        });
}

// Get CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(";").map(c => c.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith("csrftoken=")) {
            return decodeURIComponent(cookie.substring(10));
        }
    }
    return null;
}

// Apply saved ratings on page load (for movies already on page)
document.addEventListener("DOMContentLoaded", () => {
    const containers = document.querySelectorAll(".star-rating");
    containers.forEach(container => {
        const movieId = container.dataset.movie;
        renderStars(container, movieId);
    });
});