# 🔐 Secure Auth & User Management API + Filesearch Engine

Uma API RESTful robusta para autenticação segura, gestão de utilizadores e busca avançada de arquivos, desenvolvida com **FastAPI**, **SQLAlchemy** e **Pydantic**.

O projeto combina um sistema completo de autenticação baseada em JWT com um motor avançado de indexação e pesquisa de arquivos, incluindo suporte à extração de metadados EXIF e coordenadas GPS de imagens.

---

# 📖 Visão Geral

Este projeto foi desenvolvido com foco em:

- Segurança e autenticação moderna
- Arquitetura limpa e modular
- Validação rigorosa de dados
- Busca avançada de arquivos
- Extração de metadados EXIF
- Extração de coordenadas GPS
- Facilidade de manutenção
- Escalabilidade
- Testes automatizados

---

# ✨ Principais Funcionalidades

## 🔑 Autenticação e Gestão de Utilizadores

- Registro de utilizadores
- Login seguro
- Geração de tokens JWT
- Rotas protegidas
- Hashing de palavras-passe com Bcrypt
- Validação com Pydantic v2
- Controle de acesso autenticado

## 🔍 Filesearch Engine

- Varredura de diretórios
- Indexação automática de arquivos
- Extração de metadados EXIF
- Extração de coordenadas GPS
- Pesquisa dinâmica por múltiplos critérios
- Consultas otimizadas com SQLAlchemy
- Endpoints protegidos por JWT

---

# 🏗️ Arquitetura do Projeto

O sistema segue uma arquitetura modular baseada em separação de responsabilidades.

```text
Cliente
   │
   ▼
FastAPI Routers
   │
   ▼
Services
   │
   ▼
SQLAlchemy ORM
   │
   ▼
SQLite Database
```

### Organização das Camadas

```text
Routers     → Endpoints da API
Services    → Regras de negócio
Schemas     → Validação de dados
Models      → Estrutura de dados
Security    → JWT e Bcrypt
Filesearch  → Scanner, Indexador e Busca
```

---

# 🚀 Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Pydantic v2
- PyJWT
- Bcrypt
- Pillow
- Uvicorn
- Pytest

---

# 📁 Estrutura do Projeto

```text
secure-auth-api/
│
├── app/
│   │
│   ├── filesearch/
│   │   ├── cli.py
│   │   ├── models.py
│   │   │
│   │   └── services/
│   │       ├── fs_scanner.py
│   │       ├── exif_extractor.py
│   │       ├── indexer.py
│   │       └── search_engine.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── filesearch.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
│
├── tests/
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

# ⚙️ Instalação

## Pré-requisitos

- Python 3.12 ou superior
- Git

---

## Clonando o Projeto

```bash
git clone https://github.com/Gabriel31Cezar/secure-auth-api.git

cd secure-auth-api
```

---

## Criando o Ambiente Virtual

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Instalando Dependências

```bash
pip install -r requirements.txt
```

---

# 🔧 Configuração

Caso utilize variáveis de ambiente:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# ▶️ Executando a API

```bash
uvicorn app.main:app --reload
```

Aplicação disponível em:

```text
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 🔐 Fluxo de Autenticação JWT

## 1. Registrar Utilizador

```http
POST /auth/register
```

## 2. Realizar Login

```http
POST /auth/login
```

Resposta:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

## 3. Utilizar o Token

```http
Authorization: Bearer <token>
```

---

# 🛠️ Endpoints da API

## Sistema

| Método | Endpoint |
|----------|----------|
| GET | `/` |
| GET | `/health` |

## Auth

| Método | Endpoint |
|----------|----------|
| POST | `/auth/register` |
| POST | `/auth/login` |

## Users

| Método | Endpoint |
|----------|----------|
| GET | `/users/me` |

## Filesearch

| Método | Endpoint |
|----------|----------|
| POST | `/filesearch/scan` |
| POST | `/filesearch/search` |

---

# 🔎 Utilizando o Filesearch Engine

## Scan de Diretórios

Endpoint responsável por realizar varredura de diretórios e indexação dos arquivos encontrados.

```http
POST /filesearch/scan
```

---

## Busca de Arquivos

Endpoint responsável pela pesquisa de arquivos previamente indexados.

```http
POST /filesearch/search
```

---

## Recursos Disponíveis

- Busca por nome de arquivo
- Busca por extensão
- Busca por caminho
- Busca por metadados EXIF
- Busca por coordenadas GPS
- Combinação de filtros avançados

---

# 📸 Extração EXIF

O sistema suporta a leitura de metadados EXIF presentes em imagens compatíveis.

Exemplos:

- Data de captura
- Fabricante da câmera
- Modelo da câmera
- Resolução
- Informações técnicas da imagem

---

# 🌍 Geolocalização GPS

Quando disponíveis nos metadados EXIF, as coordenadas GPS são extraídas e armazenadas para futuras consultas.

Dados suportados:

- Latitude
- Longitude
- Conversão para formato decimal

---

# 🧪 Testes Automatizados

A suíte de testes cobre:

- Registro de utilizadores
- Login
- Autenticação JWT
- Rotas protegidas
- Scanner de arquivos
- Indexação
- Search Engine
- Endpoints Filesearch
- Fluxos de integração

---

## Executar Todos os Testes

```bash
pytest
```

---

## Executar com Detalhamento

```bash
pytest -v
```

---

# 🔒 Recursos de Segurança

- JWT Authentication
- Password Hashing com Bcrypt
- Rotas protegidas
- Dependency Injection
- Validação Pydantic
- Tratamento consistente de erros
- Arquitetura modular
- Separação de responsabilidades

---

# 📈 Roadmap

## v1.1

- Paginação de resultados
- Ordenação avançada
- Melhorias na documentação

## v1.2

- Cache de consultas
- Tarefas assíncronas
- Melhorias de desempenho

## Futuro

- Elasticsearch
- Dashboard Administrativo
- Estatísticas de Indexação
- Sistema de Monitoramento

---

# 🤝 Contribuição

Crie uma branch para sua alteração:

```bash
git checkout -b minha-feature
```

Realize suas alterações e faça o commit:

```bash
git commit -m "feat: nova funcionalidade"
```

Envie para o repositório remoto:

```bash
git push origin minha-feature
```

Depois abra um Pull Request.

---

# 📄 Licença

Este projeto está licenciado sob a licença MIT.

Consulte o arquivo:

```text
LICENSE
```

---

# 👨‍💻 Autor

**Gabriel Cezar**

Projeto desenvolvido para estudo, evolução técnica e construção de uma API segura de autenticação integrada a um motor avançado de pesquisa e indexação de arquivos.