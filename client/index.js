const form = document.querySelector("form");
const resultsDiv = document.querySelector("#results");
const spinner = document.querySelector("#spinner");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = e.target.search.value;
  resultsDiv.innerHTML = "";
  try {
    spinner.classList.toggle("hide");
    let r = await fetch(`http://127.0.0.1:8000/${query}`);
    let { results } = await r.json();
    for (let { title, url, similarity } of results) {
      resultsDiv.innerHTML += `<div class='card'>
            <a href=${url} target='_blank'>${title}</a>
            <div>${(100 * similarity).toFixed(2)}%</div>
        </div>`;
    }
  } catch (e) {
    console.error(e);
  } finally {
    spinner.classList.toggle("hide");
  }
});
