# chatbot-ai (backend)

**chatbot-ai** is a backend project that implements a **Retrieval-Augmented Generation (RAG)** system using **FastAPI**, **LangChain**, **OpenAI**, and **Chroma DB**.
It includes secure **user authentication**, **document ingestion**, **AI-powered chat responses**, and a **CI pipeline with automated testing** following the **GitFlow** branching model.

---

## 🔹 Features

- 🔐 **User Authentication** with JWT and password hashing
- 📚 **Document Ingestion**: store PDFs or text embeddings in Chroma DB
- 💬 **Chat with AI** using LangChain and OpenAI’s API
- 🧪 **Automated Testing** using pytest
- 🚀 **GitFlow & CI Pipeline** with GitHub Actions
- 🧱 **Modular FastAPI Architecture** (routes, services, models, config)

---

## 🔹 Tech Stack

| Layer                 | Technology                        |
| --------------------- | --------------------------------- |
| **Backend Framework** | FastAPI                           |
| **Database**          | PostgreSQL + SQLAlchemy + Alembic |
| **Vector Store**      | Chroma DB                         |
| **AI Engine**         | OpenAI via LangChain              |
| **Auth & Security**   | JWT + Passlib                     |
| **Testing**           | pytest + httpx + pytest-cov       |
| **CI/CD**             | GitHub Actions                    |

---

## 🔹 Folder Structure

```
chatbot-ai/
│
├── main.py               # FastAPI entry point
├── core/
│   └── config.py         # Environment variables and global settings
├── models/               # SQLAlchemy models
├── routes/               # FastAPI routers (auth, RAG, etc.)
├── services/             # Business logic (authentication, RAG processing)
├── tests/                # Unit and integration tests
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_rag.py
└── .github/
    └── workflows/
        └── test-pipeline.yml
```

---

## 🔹 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/chatbot-ai.git
cd chatbot-ai
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_ai
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret
```

### 5️⃣ Apply migrations

```bash
alembic upgrade head
```

### 6️⃣ Start the development server

```bash
uvicorn main:app --reload
```

Then visit 👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🔹 API Overview

### 🧑‍💻 Authentication

**Register user**

```
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Login**

```
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

✅ Returns a JWT token for authentication.

---

### 📚 Document Ingestion

Upload a file and generate embeddings:

```
POST /rag/upload
Headers: Authorization: Bearer <JWT>
Body: file (PDF or TXT)
```

---

### 💬 Ask a Question

Query the knowledge base using OpenAI:

```
POST /rag/query
Headers: Authorization: Bearer <JWT>
Body: { "question": "What is this document about?" }
```

---

## 🔹 GitFlow Workflow

This repository follows **GitFlow** for clean development and releases:

| Branch      | Purpose                    |
| ----------- | -------------------------- |
| `main`      | Production-ready code      |
| `develop`   | Integration/testing branch |
| `feature/*` | New features               |
| `release/*` | Pre-release versions       |
| `hotfix/*`  | Quick fixes for production |

### Example:

```bash
git checkout -b feature/auth develop
# Develop feature
git commit -m "Add user authentication"
git push origin feature/auth

# Merge into develop after review
git checkout develop
git merge feature/auth
```

---

## 🔹 Testing

### Run all tests

```bash
pytest -v
```

### Run with coverage

```bash
pytest --cov=services --cov=routes --cov-report=term-missing
```

### Generate HTML coverage report

```bash
pytest --cov=services --cov=routes --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the report.

---

## 🔹 Continuous Integration (CI)

The CI pipeline runs automatically using **GitHub Actions** on every push or pull request to:

- `main`
- `develop`
- `feature/*`

### 📁 `.github/workflows/test-pipeline.yml`

The workflow:

- Installs dependencies
- Runs all unit tests
- Reports coverage
- Blocks merging if tests fail

View the results under the **Actions** tab in GitHub.

---

## 🔹 Future Enhancements

- Docker support for easy deployment
- Async task queue with Celery or FastAPI background tasks
- Admin dashboard for user management
- Streaming chat responses
- API rate limiting

---

## 🔹 Contributing

1. Fork this repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push and open a Pull Request

---

## 🔹 License

This project is licensed under the **MIT License**.
