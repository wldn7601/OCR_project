document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const overlay = document.getElementById("loadingOverlay");
  const btn = document.getElementById("uploadBtn");

  if (form && overlay && btn) {
    form.addEventListener("submit", () => {
      overlay.style.display = "block";
      btn.disabled = true;
    });
  }
});
