// Troca de abas e validação dos formulários (sem envio à API nesta etapa)
(function () {
  const tabLogin = document.getElementById("tab-login");
  const tabRegister = document.getElementById("tab-register");
  const formLogin = document.getElementById("form-login");
  const formRegister = document.getElementById("form-register");
  const alertBox = document.getElementById("alert");

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

  tabLogin.addEventListener("click", () => showTab(true));
  tabRegister.addEventListener("click", () => showTab(false));

  [formLogin, formRegister].forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const firstInvalid = validateForm(form);
      if (firstInvalid !== null) {
        firstInvalid.focus();
        showAlert("Corrija os campos destacados.", "error");
        return;
      }
      showAlert("Dados válidos. O envio para a API será ligado na próxima etapa.", "success");
    });

    // Ao digitar, remove o erro do campo para não ficar cobrando enquanto corrige
    rules[form.id].forEach((rule) => {
      const input = document.getElementById(rule.id);
      input.addEventListener("input", () => setError(input, ""));
    });
  });
})();