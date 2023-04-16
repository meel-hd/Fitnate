const oldTheme = localStorage.getItem("theme") || "light"; // default to light theme if no theme is set in local storage

// if the theme is dark, add the dark class to the body
if (oldTheme === "dark") {
  document.body.classList.add("bg-stone-950");
  document.body.classList.add("text-white");
}

// toggle the theme when the button is clicked
function switchTheme() {
  document.body.classList.toggle("bg-stone-950");
  document.body.classList.toggle("text-white");
  if (oldTheme === "light") {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}
