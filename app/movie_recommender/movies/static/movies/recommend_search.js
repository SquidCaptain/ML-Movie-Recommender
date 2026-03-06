const searchInput = document.getElementById("search");
const resultsDiv = document.getElementById("results");
const selectedDiv = document.getElementById("selected");

searchInput.addEventListener("keyup", function() {

    fetch(`/search/?q=${this.value}`)
        .then(response => response.json())
        .then(data => {

            resultsDiv.innerHTML = "";

            data.forEach(movie => {

                const div = document.createElement("div");
                div.classList.add("movie-card");

                div.innerHTML = `
                    <img src="https://image.tmdb.org/t/p/w200${movie.poster}">
                    <p>${movie.title}</p>
                    <button class="btn" type="button" onclick="selectMovie('${movie.title}')">Select</button>
                `;

                resultsDiv.appendChild(div);

            });

        });

});


function selectMovie(title) {

    const input = document.createElement("input");

    input.type = "hidden";
    input.name = "favorites";
    input.value = title;

    selectedDiv.appendChild(input);

    alert(title + " added!");

}