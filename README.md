# DocuMind AI

**An AI-powered document assistant with Retrieval-Augmented Generation (RAG) and intelligent interview scheduling.**

DocuMind AI is a Python backend application that allows users to upload PDF and TXT documents, retrieve relevant information through semantic search, and ask questions using an LLM. It also includes a conversational interview scheduling system that collects candidate details and stores confirmed bookings.

## Features

### Document Processing
- Upload PDF and TXT documents.
- Extract text from uploaded documents.
- Support two chunking strategies: fixed-size and recursive.
- Generate text embeddings using Sentence Transformers.
- Store and retrieve document vectors using Qdrant.
- Store document metadata in PostgreSQL.

### AI-Powered Question Answering
- Custom Retrieval-Augmented Generation (RAG) pipeline.
- Semantic search for relevant document context.
- Generate context-aware answers using Llama 3 through Ollama.
- Support conversational interactions with Redis-based chat memory.

### Interview Scheduling
- Conversational interview booking workflow.
- Extract candidate name, email, preferred date, and time.
- Identify missing booking information and ask follow-up questions.
- Request confirmation before saving a booking.
- Store confirmed interview details in PostgreSQL.
- Redis-based booking status tracking to help prevent duplicate bookings.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM & Migrations | SQLAlchemy, Alembic |
| Vector Database | Qdrant |
| Cache & Chat Memory | Redis |
| LLM | Ollama, Llama 3 |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Document Extraction | pypdf |
| Text Chunking | LangChain Text Splitters |



## ⚙️ Getting Started

### Prerequisites

Install the following before running the application:

- Python 3.13
- PostgreSQL
- Docker Desktop
- Ollama

### 1. Clone the repository

```bash
git clone https://github.com/Bhus7/documind-ai.git
cd documind-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
```

Replace the placeholders with your PostgreSQL credentials and database name.

### 5. Start Redis and Qdrant

Run Redis:

```bash
docker run -d --name redis -p 6379:6379 redis
```

Run Qdrant:

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### 6. Start Ollama

Install Ollama and download the Llama 3 model:

```bash
ollama pull llama3
```

Start the Ollama service:

```bash
ollama serve
```

### 7. Apply database migrations

```bash
alembic upgrade head
```

### 8. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## 🔌 API Documentation

DocuMind AI provides REST API functionality for:

- Document upload and ingestion.
- Document-based conversational question answering.
- AI-powered interview scheduling.

Explore the available endpoints and test requests through the interactive Swagger documentation at `/docs`.

##  Security

- Environment variables are used for database configuration.
- Sensitive configuration files such as `.env` are excluded from version control.
- Virtual environments and Python cache files are excluded from Git.

##🎯 Project Goals

This project demonstrates practical backend development and AI integration, including:

- REST API development with FastAPI.
- Document ingestion and processing pipelines.
- Vector embeddings and semantic search.
- Custom Retrieval-Augmented Generation.
- Database design and migrations.
- Conversational memory using Redis.
- LLM-powered workflow automation.

##  Author

**Bhusan Bohara**

GitHub: [@Bhus7](https://github.com/Bhus7)

---

*Built with Python, FastAPI, and AI-powered technologies.*
