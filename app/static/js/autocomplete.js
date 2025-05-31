document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("location-input");
    const resultsBox = document.getElementById("autocomplete-results");

    input.addEventListener("input", function () {
        const query = input.value;
        if (query.length < 2) {
            resultsBox.innerHTML = "";
            return;
        }

        fetch(`/api/autocomplete/?query=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                resultsBox.innerHTML = "";
                data.forEach(city => {
                    const div = document.createElement("div");
                    div.classList.add("autocomplete-item");
                    div.textContent = city;
                    div.addEventListener("click", function () {
                        input.value = city;
                        resultsBox.innerHTML = "";
                    });
                    resultsBox.appendChild(div);
                });
            });
    });

    // закрытие по клику вне
    document.addEventListener("click", function (e) {
        if (!resultsBox.contains(e.target) && e.target !== input) {
            resultsBox.innerHTML = "";
        }
    });
});
