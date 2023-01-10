const form = document.querySelector("form");
const resultsDiv = document.querySelector("#results");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = e.target.search.value;
  let r = await fetch(`http://127.0.0.1:8000/${query}`);
  resultsDiv.append(JSON.stringify(await r.json()));
});
