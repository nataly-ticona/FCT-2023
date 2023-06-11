

document.addEventListener("DOMContentLoaded", function () {
  const main = document.getElementsByTagName("main")[0];
  main.style.display="none"
  const loader = document.getElementById("loader");
  loader.style.display = "block";
});

window.addEventListener("load", function () {
  loader.style.display = "none";
  const main = document.getElementsByTagName("main")[0];
  main.style.display = "block"
});