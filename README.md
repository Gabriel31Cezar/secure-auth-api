# 🔐 Secure Auth & User Management API

Uma API RESTful robusta e segura para gestão de utilizadores e autenticação baseada em tokens JWT, desenvolvida com **FastAPI**, **SQLAlchemy** e **Pydantic**.

O projeto conta com hashing seguro de palavras-passe via **Bcrypt**, arquitetura modular baseada em rotas e documentação interativa automática gerada pelo Swagger UI.

---

## 🚀 Tecnologias Utilizadas

- **[Python 3.12 / 3.14](https://www.python.org/)** — Linguagem principal
- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web de alta performance
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para mapeamento e interação com a base de dados SQLite
- **[Pydantic v2](https://docs.pydantic.dev/)** — Validação de dados e definições de schemas
- **[PyJWT](https://pyjwt.readthedocs.io/)** — Geração e verificação de tokens de acesso JWT
- **[Bcrypt](https://pypi.org/project/bcrypt/)** — Algoritmo de hashing seguro para armazenamento de palavras-passe
- **[Uvicorn](https://www.uvicorn.org/)** — Servidor ASGI para execução da aplicação

---

## 📁 Estrutura do Projeto

```text
secure-auth-api/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py         # Endpoints de registo e login
│   │   └── users.py        # Endpoints protegidos de utilizadores
│   ├── __init__.py
│   ├── config.py           # Configurações globais com Pydantic Settings
│   ├── database.py         # Conexão e sessão do SQLAlchemy (SQLite)
│   ├── main.py             # Ponto de entrada da aplicação FastAPI
│   ├── models.py           # Modelos de dados do banco de dados (User)
│   ├── schemas.py          # Schemas Pydantic para requisições e respostas
│   └── security.py        # Lógica de hashing bcrypt e utilitários JWT
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

## 🛠️ Como Executar o Projeto Localmente

### Pré-requisitos
- Python instalado na sua máquina (versão 3.10 ou superior).
- Git configurado.

### Passos para instalação:

1. **Clonar o repositório:**
   git clone https://github.com/Gabriel31Cezar/secure-auth-api.git
   cd secure-auth-api

2. **Criar e ativar o ambiente virtual (`.venv`):**
   - **Windows:**
     python -m venv .venv
     .\.venv\Scripts\activate
   - **Linux/macOS:**
     python3 -m venv .venv
     source .venv/bin/activate

3. **Instalar as dependências:**
   pip install -r requirements.txt

4. **Executar a aplicação com o Uvicorn:**
   uvicorn app.main:app --reload

5. **Acessar a documentação interativa (Swagger UI):**
   Abra o seu navegador e aceda a: `http://127.0.0.1:8000/docs`

---

## 🛠️ Endpoints da API

| Método | Rota | Autenticação | Descrição |
| :--- | :--- | :---: | :--- |
| GET | / | Não | Retorna mensagem de status e verificação inicial da API. |
| GET | /health | Não | Endpoint para health check da aplicação. |
| POST | /auth/register | Não | Regista um novo utilizador no sistema. |
| POST | /auth/login | Não | Autentica o utilizador e gera o token de acesso JWT. |
| GET | /users/me | **Sim (JWT)** | Retorna os dados do utilizador atualmente autenticado. |

---

## 🔒 Testando as Rotas Protegidas no Swagger UI

1. Aceda a `http://127.0.0.1:8000/docs`.
2. Faça o registo de um utilizador na rota `POST /auth/register`.
3. Autentique-se na rota `POST /auth/login` para receber o `access_token`.
4. Clique no botão verde **Authorize** (com o ícone de cadeado) no canto superior direito da tela.
5. Insira as credenciais no formulário do pop-up e clique em **Authorize**.
6. Agora pode testar o endpoint protegido `GET /users/me`!

---

## 📄 Licença

Este projeto está sob a licença MIT.
