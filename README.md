# chatbot-ai (backend)

**chatbot-ai** is a customizable **Retrieval-Augmented Generation (RAG)** system built with **FastAPI**, **LangChain**, and **OpenAI**.
It allows users to upload documents, ask questions, and receive AI-generated answers based on their own data. The system includes **user authentication**, **JWT-secured endpoints**, and a **CI pipeline with automated testing**, making it production-ready and portfolio-grade.

---

## 🔹 Features

- **User Authentication** — Secure registration and login using JWT.
- **Document Ingestion** — Upload PDF or text files and store embeddings in **Chroma DB**.
- **RAG Chat** — Query your uploaded documents using **OpenAI** + **LangChain**.
- **Customizable AI Pipeline** — Configure retrieval parameters (`top_k`, model selection, etc.).
- **Automated Tests** — Integrated unit tests with **pytest** and GitHub Actions.
- **GitFlow Workflow** — Organized branching model for clean development and releases.
- **Modular Architecture** — Clear separation of routes, services, models, and core logic.

---

## 🔹 Tech Stack

| Layer                  | Technology                        |
| ---------------------- | --------------------------------- |
| **Backend**            | FastAPI (Python)                  |
| **Database**           | PostgreSQL + SQLAlchemy + Alembic |
| **Vector Store**       | Chroma DB                         |
| **AI Model**           | OpenAI (via LangChain)            |
| **Auth**               | JWT + Passlib                     |
| **Testing**            | pytest + httpx + pytest-cov       |
| **CI/CD**              | GitHub Actions                    |
| **Frontend (planned)** | Next.js + Tailwind + Zustand      |

---

## 🔹 Folder Structure

```
ROOT/
│
├── main.py               # FastAPI entry point
├── core/
│   └── config.py         # Environment variables and app settings
├── models/               # SQLAlchemy models
├── routes/               # API routes (auth, RAG, etc.)
├── services/             # Business logic (auth, embeddings, etc.)
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
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
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

### 5️⃣ Apply database migrations

```bash
alembic upgrade head
```

### 6️⃣ Start the server

```bash
uvicorn main:app --reload
```

Access the API at 👉 `http://localhost:8000`

---

## 🔹 Usage

### 🔐 Register a user

```
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123"
}
```

### 🔑 Login

```
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

➡️ Returns a JWT token.

### 📤 Upload a document

```
POST /rag/upload
Headers: Authorization: Bearer <JWT>
Body: file (PDF or TXT)
```

### 💬 Ask a question

```
POST /rag/query
Headers: Authorization: Bearer <JWT>
Body: { "question": "What is this document about?" }
```

---

## 🔹 GitFlow Workflow

This project follows the **GitFlow branching model** for organized development:

| Branch      | Purpose                                   |
| ----------- | ----------------------------------------- |
| `main`      | Production-ready code                     |
| `develop`   | Integration and testing branch            |
| `feature/*` | Individual features (e.g. `feature/auth`) |
| `release/*` | Pre-release versions                      |
| `hotfix/*`  | Emergency fixes for production            |

### Example workflow:

```bash
git checkout -b feature/auth develop
# ... develop your feature
git commit -m "Add user authentication"
git push origin feature/auth

# Merge to develop
git checkout develop
git merge feature/auth
```

---

## 🧪 Testing

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

Then open `htmlcov/index.html` in your browser.

---

## 🔹 Continuous Integration (CI)

GitHub Actions automatically runs your test suite on every push or pull request to:

- `main`
- `develop`
- `feature/*`

### 📁 `.github/workflows/test-pipeline.yml`

This workflow:

- Installs dependencies
- Runs all tests with coverage
- Blocks merge if tests fail

View pipeline results in your GitHub repo under **Actions**.

---

## 🔹 Future Enhancements

- Frontend (Next.js + Tailwind + Zustand)
- Streaming chat responses
- Support for additional document types (CSV, DOCX)
- Multi-user isolation for Chroma DB
- Docker deployment for backend and vector store

---

## 🔹 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add your feature"`)
4. Push and open a Pull Request

---

## 🔹 License

This project is licensed under the **MIT License**.
