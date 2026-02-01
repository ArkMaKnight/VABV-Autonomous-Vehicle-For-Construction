const btn = document.getElementById("toggleSidebar");

btn.addEventListener("click", () => {
  document.body.classList.toggle("sidebar-collapsed");
});
