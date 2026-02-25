# 🥗 Human Nutrition AI

An AI-powered nutrition assistant using **RAG (Retrieval-Augmented Generation)** to answer questions about human nutrition based on scientific literature.

## ✨ Features

- 🧠 **Intelligent Q&A**: Ask any nutrition-related question and get accurate, context-aware answers
- 🎨 **Premium UI**: Modern glassmorphism design with smooth animations
- ⚡ **Fast Responses**: Pre-loaded RAG pipeline for quick response times
- 📊 **OpenAPI Docs**: Built-in API documentation at `/docs`
- 🐳 **Docker Ready**: Easy deployment with Docker Compose

## 🏗️ Project Structure

```
RAG_First_Project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   └── config.py        # Settings & environment
│   ├── services/
│   │   └── rag_service.py   # RAG chain logic
│   └── models/
│       └── schemas.py       # Pydantic models
├── static/
│   └── index.html           # Premium UI
├── data/
│   └── HumanNutrition.pdf   # Source document
├── .env.example             # Environment template
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py                   # Entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/) with `tinyllama` model

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd RAG_First_Project

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### Running Locally

```bash
# Start Ollama (if not running)
ollama serve

# Pull the model
ollama pull tinyllama

# Run the application
python run.py
```

Open http://127.0.0.1:8001 in your browser.

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend UI |
| `/health` | GET | Health check |
| `/api/rag` | POST | Ask a question |
| `/docs` | GET | OpenAPI documentation |

### Example Request

```bash
curl -X POST http://127.0.0.1:8001/api/rag \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main sources of Vitamin C?"}'
```

## ⚙️ Configuration

All settings can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 127.0.0.1 | Server host |
| `PORT` | 8001 | Server port |
| `DEBUG` | false | Enable debug mode |
| `LLM_MODEL` | tinyllama | Ollama model name |
| `CHUNK_SIZE` | 800 | Document chunk size |

## 🛠️ Tech Stack

- **Backend**: FastAPI, LangChain, Ollama
- **Embeddings**: HuggingFace sentence-transformers
- **Vector Store**: FAISS
- **Frontend**: Vanilla JS with glassmorphism UI

## 📝 License

MIT License