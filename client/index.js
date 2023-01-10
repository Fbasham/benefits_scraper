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
    resultsDiv.append(JSON.stringify(await r.json()));
  } catch (e) {
    console.error(e);
  } finally {
    spinner.classList.toggle("hide");
  }
});
