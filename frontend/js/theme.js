// Alternador de tema (Dark/Light)
(function () {
  const STORAGE_KEY = "theme";
  const root = document.documentElement;
  const button = document.getElementById("theme-toggle");

  function getInitialTheme() {
    let saved = null;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      saved = null;
    }
    if (saved === "dark" || saved === "light") {
      return saved;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    button.textContent = theme === "dark" ? "Modo claro" : "Modo escuro";
  }

  function toggleTheme() {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (error) {
      // Se o navegador bloquear o armazenamento, o tema vale só nesta página.
    }
  }

  applyTheme(getInitialTheme());
  button.addEventListener("click", toggleTheme);
})();