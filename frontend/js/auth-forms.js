// Troca de abas, validação, cadastro, autenticação, perfil e status da API
(function () {
// ===== Configuração da API =====
const API_BASE_URL = "http://127.0.0.1:8000";
const TOKEN_KEY = "access_token";

  // ===== Elementos da página =====
  const tabLogin = document.getElementById("tab-login");
  const tabRegister = document.getElementById("tab-register");
  const formLogin = document.getElementById("form-login");
  const formRegister = document.getElementById("form-register");
  const alertBox = document.getElementById("alert");
  const authCard = document.getElementById("auth-card");
  const userPanel = document.getElementById("user-panel");
  const userUsername = document.getElementById("user-username");
  const userEmail = document.getElementById("user-email");
  const userToken = document.getElementById("user-token");
  const logoutBtn = document.getElementById("logout-btn");
  const loginButton = formLogin.querySelector('button[type="submit"]');
  const registerButton = formRegister.querySelector('button[type="submit"]');
  const apiStatus = document.getElementById("api-status");
  const apiStatusText = apiStatus.querySelector(".status-text");

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

  // ===== Status da API (health check) =====

  async function checkApiHealth() {
    try {
      const response = await fetch(API_BASE_URL + "/health");
      setApiStatus(response.ok);
    } catch (error) {
      // Sem resposta da API (backend desligado ou erro de rede)
      setApiStatus(false);
    }
  }

  function setApiStatus(isOnline) {
    apiStatus.classList.toggle("online", isOnline);
    apiStatus.classList.toggle("offline", !isOnline);
    apiStatusText.textContent = isOnline ? "API online" : "API offline";
  }

  // ===== Comunicação com a API =====

  // Lê a resposta JSON e lança erro com a mensagem da API quando não for sucesso
  async function readResponse(response, fallbackMessage) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const message = typeof data.detail === "string" ? data.detail : fallbackMessage;
      const error = new Error(message);
      error.status = response.status;
      throw error;
    }
    return data;
  }

  // O FastAPI espera dados de formulário com os campos "username" e "password", não JSON
  async function requestLogin(username, senha) {
    const body = new URLSearchParams();
    body.append("username", username);
    // noinspection SpellCheckingInspection
    body.append("password", senha);

    const response = await fetch(API_BASE_URL + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body
    });

    return readResponse(response, "Não foi possível fazer a entrada.");
  }

  // O cadastro usa JSON, conforme o schema UserCreate da API
  async function requestRegister(username, email, senha) {
    const response = await fetch(API_BASE_URL + "/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, username: username, password: senha })
    });

    return readResponse(response, "Não foi possível criar a conta.");
  }

  // Busca os dados do usuário autenticado; a chave JWT vai no cabeçalho Authorization
  async function loadProfile(token) {
    try {
      const response = await fetch(API_BASE_URL + "/users/me", {
        headers: { Authorization: "Bearer " + token }
      });

      if (response.status === 401) {
        // Chave expirada ou inválida: encerra a sessão e volta para o login
        logout();
        showAlert("Sua sessão expirou. Entre novamente.", "error");
        return;
      }

      const user = await response.json().catch(() => null);
      if (!response.ok || !user) {
        showAlert("Não foi possível carregar seus dados.", "error");
        return;
      }
      showPanel(user, token);
    } catch (error) {
      showConnectionOrApiError(error);
    }
  }

  async function handleLogin() {
    const username = document.getElementById("login-username").value.trim();
    const senha = document.getElementById("login-password").value;

    setButtonLoading(loginButton, true, "Entrando...", "Entrar");
    try {
      const data = await requestLogin(username, senha);
      sessionStorage.setItem(TOKEN_KEY, data.access_token);
      formLogin.reset();
      await loadProfile(data.access_token);
    } catch (error) {
      showConnectionOrApiError(error);
    } finally {
      setButtonLoading(loginButton, false, "Entrando...", "Entrar");
    }
  }

  async function handleRegister() {
    const username = document.getElementById("reg-username").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const senha = document.getElementById("reg-password").value;

    setButtonLoading(registerButton, true, "Criando conta...", "Criar conta");
    try {
      await requestRegister(username, email, senha);
      formRegister.reset();
      showTab(true);
      document.getElementById("login-username").value = username;
      document.getElementById("login-password").focus();
      showAlert("Conta criada com sucesso. Agora entre com sua senha.", "success");
    } catch (error) {
      showConnectionOrApiError(error);
    } finally {
      setButtonLoading(registerButton, false, "Criando conta...", "Criar conta");
    }
  }

  function showConnectionOrApiError(error) {
    if (error instanceof TypeError) {
      // Erro de rede: o navegador não conseguiu falar com a API
      showAlert("Não foi possível conectar à API em " + API_BASE_URL + ". Confira se o backend está rodando.", "error");
    } else {
      showAlert(error.message, "error");
    }
  }

  function setButtonLoading(button, isLoading, loadingText, normalText) {
    button.disabled = isLoading;
    button.textContent = isLoading ? loadingText : normalText;
  }

  // ===== Painel do usuário =====

  function showPanel(user, token) {
    clearAlert();
    authCard.classList.add("hidden");
    userPanel.classList.remove("hidden");
    userUsername.textContent = user.username;
    userEmail.textContent = user.email;
    userToken.textContent = token;
  }

  function showAuthCard() {
    userPanel.classList.add("hidden");
    authCard.classList.remove("hidden");
    userUsername.textContent = "-";
    userEmail.textContent = "-";
    userToken.textContent = "-";
  }

  function logout() {
    sessionStorage.removeItem(TOKEN_KEY);
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
        await handleRegister();
      }
    });

    // Ao digitar, remove o erro do campo
    rules[form.id].forEach((rule) => {
      const input = document.getElementById(rule.id);
      input.addEventListener("input", () => setError(input, ""));
    });
  });

  logoutBtn.addEventListener("click", logout);

  // Se já existe uma chave salva nesta aba, busca o perfil direto
  const savedToken = sessionStorage.getItem(TOKEN_KEY);
  if (savedToken) {
    authCard.classList.add("hidden");
    loadProfile(savedToken).catch(() => showAlert("Não foi possível carregar seus dados.", "error"));
  }

  // Verifica a API ao abrir a página
  checkApiHealth().catch(() => setApiStatus(false));
})();