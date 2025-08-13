# URL Shortener

> A service for creating short links.

[![Python checks 🐍](https://github.com/Nottezz/fastapi-url-shortener/actions/workflows/python-check.yml/badge.svg?event=pull_request)](https://github.com/Nottezz/fastapi-url-shortener/actions/workflows/python-check.yml)
[![codecov](https://codecov.io/github/Nottezz/fastapi-url-shortener/graph/badge.svg?token=433SJRXNNI)](https://codecov.io/github/Nottezz/fastapi-url-shortener)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![Python version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blueviolet)](http://mypy-lang.org/)
[![code style: ruff](https://img.shields.io/badge/code%20style-ruff-blue)](https://docs.astral.sh/ruff/)
[![uv: managed](https://img.shields.io/badge/dependencies-managed%20with%20uv-yellowgreen)](https://github.com/astral-sh/uv)

## 🧑‍💻 Getting Started

### 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Nottezz/fastapi-url-shortener.git
   cd url_shortener


2. Mark the `url_shortener` directory as "Sources Root" in your IDE (for better imports).

---

### 📦 Install Dependencies

Use [`uv`](https://github.com/astral-sh/uv) to install packages:

```bash
uv install
```
---

### ⚙️ Configure Pre-commit Hooks

Install and activate pre-commit:

```bash
pre-commit install
```

This ensures formatting, linting, and other checks before each commit.

---

### 🚀 Run Development Server

1. Ensure you're in the working directory:

   ```bash
   cd url_shortener
   ```

2. Make sure Redis is running:

   ```bash
   docker run -d -p 6379:6379 redis
   ```

3. Start the FastAPI dev server:

   ```bash
   fastapi dev
   ```

The server will be available at `http://localhost:8000`.

---

### ✅ Running Tests

1. Make sure that the Redis test container is running.:

   ```bash
   docker run -d -p 6380:6380 redis
   ```
2. Set env variables: REDIS_PORT=6380;TESTING=1


3. Run the test suite:

   ```bash
   pytest
   ```

---

## 👨‍🔧 For Developers

* Use a virtual environment (`uv`, `venv`, or `poetry`) to manage dependencies.
* Follow PEP8 style guidelines (auto-enforced via `pre-commit`).
* Use descriptive commit messages (consider [Conventional Commits](https://www.conventionalcommits.org/)).
* Document public endpoints and services clearly with docstrings and OpenAPI schemas.

---
