// Troca de abas, validação e autenticação na API
(function () {
  // ===== Configuração da API =====
  const API_BASE_URL = "http://127.0.0.1:8000";
  const TOKEN_KEY = "access_token";
  const USER_KEY = "username";

  // ===== Elementos da página =====
  const tabLogin = document.getElementById("tab-login");
  const tabRegister = document.getElementById("tab-register");
  const formLogin = document.getElementById("form-login");
  const formRegister = document.getElementById("form-register");
  const alertBox = document.getElementById("alert");
  const authCard = document.getElementById("auth-card");
  const userPanel = document.getElementById("user-panel");
  const userUsername = document.getElementById("user-username");
  const userToken = document.getElementById("user-token");
  const logoutBtn = document.getElementById("logout-btn");
  const loginButton = formLogin.querySelector('button[type="submit"]');

  const USERNAME_PATTERN = /^[A-Za-z0-9_]{3,30}$/;
  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Regras de cada campo: check recebe o valor e devolve true se estiver válido
  const rules = {
    "form-login": [
      {
        id: "login-username",
        check: (value) => value.trim().length > 0,
        message: "Informe seu usuário ou e-mail."
      },
      {
        id: "login-password",
        check: (value) => value.length > 0,
        message: "Informe sua senha."
      }
    ],
    "form-register": [
      {
        id: "reg-username",
        check: (value) => USERNAME_PATTERN.test(value),
        message: "Use de 3 a 30 letras, números ou _."
      },
      {
        id: "reg-email",
        check: (value) => EMAIL_PATTERN.test(value.trim()),
        message: "Informe um e-mail válido."
      },
      {
        id: "reg-password",
        check: (value) => value.length >= 8,
        message: "A senha deve ter pelo menos 8 caracteres."
      }
    ]
  };

  // ===== Comunicação com a API =====

  // O FastAPI espera dados de formulário (campos username e senha), não JSON
  async function requestLogin(username, senha) {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", senha);

    const response = await fetch(API_BASE_URL + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const message = typeof data.detail === "string" ? data.detail : "Não foi possível fazer a entrada.";
      const error = new Error(message);
      error.status = response.status;
      throw error;
    }

    return data; // { access_token, token_type }
  }

  async function handleLogin() {
    const username = document.getElementById("login-username").value.trim();
    const senha = document.getElementById("login-password").value;

    setLoginLoading(true);
    try {
      const data = await requestLogin(username, senha);
      sessionStorage.setItem(TOKEN_KEY, data.access_token);
      sessionStorage.setItem(USER_KEY, username);
      formLogin.reset();
      showPanel(username, data.access_token);
    } catch (error) {
      if (error instanceof TypeError) {
        // Erro de rede: o navegador não conseguiu falar com a API
        showAlert("Não foi possível conectar à API em " + API_BASE_URL + ". Confira se o backend está rodando.", "error");
      } else {
        showAlert(error.message, "error");
      }
    } finally {
      setLoginLoading(false);
    }
  }

  function setLoginLoading(isLoading) {
    loginButton.disabled = isLoading;
    loginButton.textContent = isLoading ? "Entrando..." : "Entrar";
  }

  // ===== Painel do usuário =====

  function showPanel(username, token) {
    clearAlert();
    authCard.classList.add("hidden");
    userPanel.classList.remove("hidden");
    userUsername.textContent = username;
    userToken.textContent = token;
  }

  function showAuthCard() {
    userPanel.classList.add("hidden");
    authCard.classList.remove("hidden");
    userUsername.textContent = "-";
    userToken.textContent = "-";
  }

  function logout() {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    showAuthCard();
  }

  // ===== Abas, alertas e validação =====

  function showTab(isLogin) {
    formLogin.classList.toggle("hidden", !isLogin);
    formRegister.classList.toggle("hidden", isLogin);
    tabLogin.classList.toggle("active", isLogin);
    tabRegister.classList.toggle("active", !isLogin);
    tabLogin.setAttribute("aria-selected", String(isLogin));
    tabRegister.setAttribute("aria-selected", String(!isLogin));
    clearAlert();
  }

  function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = "alert " + type;
  }

  function clearAlert() {
    alertBox.textContent = "";
    alertBox.className = "alert hidden";
  }

  function setError(input, message) {
    const errorEl = document.getElementById("err-" + input.id);
    if (errorEl) {
      errorEl.textContent = message;
    }
    input.classList.toggle("invalid", Boolean(message));
    input.setAttribute("aria-invalid", String(Boolean(message)));
  }

  // Valida todos os campos do formulário e devolve o primeiro inválido (ou null)
  function validateForm(form) {
    let firstInvalid = null;
    rules[form.id].forEach((rule) => {
      const input = document.getElementById(rule.id);
      const valid = rule.check(input.value);
      setError(input, valid ? "" : rule.message);
      if (!valid && firstInvalid === null) {
        firstInvalid = input;
      }
    });
    return firstInvalid;
  }

  // ===== Eventos =====

  tabLogin.addEventListener("click", () => showTab(true));
  tabRegister.addEventListener("click", () => showTab(false));

  [formLogin, formRegister].forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const firstInvalid = validateForm(form);
      if (firstInvalid !== null) {
        firstInvalid.focus();
        showAlert("Corrija os campos destacados.", "error");
        return;
      }
      if (form === formLogin) {
        await handleLogin();
      } else {
        showAlert("Dados válidos. O cadastro na API será ligado na próxima etapa.", "success");
      }
    });

    // Ao digitar, remove o erro do campo
    rules[form.id].forEach((rule) => {
      const input = document.getElementById(rule.id);
      input.addEventListener("input", () => setError(input, ""));
    });
  });

  logoutBtn.addEventListener("click", logout);

  // Se já existe um token nesta aba (por exemplo, após F5), mostra o painel direto
  const savedToken = sessionStorage.getItem(TOKEN_KEY);
  if (savedToken) {
    showPanel(sessionStorage.getItem(USER_KEY) || "-", savedToken);
  }
})();