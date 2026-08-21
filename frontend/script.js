console.log("script.js loaded");

let backend = null;

const searchInput = document.querySelector(".search input");
const searchButton = document.querySelector(".search button");
const resultsContainer = document.querySelector(".results");


new QWebChannel(qt.webChannelTransport, function (channel) {
    backend = channel.objects.backend;

    console.log("VISTARA backend connected");
});


searchButton.addEventListener("click", () => {
    const query = searchInput.value.trim();

    console.log("Button clicked:", query);

    if (!query) {
        return;
    }

    if (!backend) {
        console.log("Backend not ready");
        return;
    }

    backend.search(query, function (results) {
        console.log("Results from Python:", results);

        resultsContainer.innerHTML = "";

        results.forEach(result => {
            const resultElement = document.createElement("div");

            resultElement.className = "result";

            resultElement.innerHTML = `
                <h3>${result.title}</h3>
                <p>${result.path}</p>
            `;

            resultElement.addEventListener("click", ()=>{
                backend.open_file(result.path)
            })

            resultsContainer.appendChild(resultElement);
        });
    });
});