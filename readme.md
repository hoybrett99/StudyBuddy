# 📚 Study Buddy - AI-Powered Study Assistant

> An intelligent RAG (Retrieval-Augmented Generation) system that transforms textbooks into an interactive Q&A assistant.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-95%25%20Coverage-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

## 🎯 Project Purpose

This project is built **purely for fun and learning!** 🚀

The main goals are:
- 📖 Learn how RAG systems actually work under the hood
- 🤖 Understand AI/ML integration in production applications
- 📱 Learn Kotlin while building the Android frontend
- 🔧 Practice building full-stack applications from scratch
- 🧪 Improve software engineering skills (testing, architecture, etc.)
- 🎨 Experiment with making complex AI accessible through simple UIs

Think of this as a learning playground where I'm exploring modern AI technologies while building something useful for students!

---

## ✨ What It Does

Upload your textbooks (PDF, Word, or text files), ask questions in natural language, and get instant answers with source citations—like having a personal tutor available 24/7!

**Example:**
```
You: "What is photosynthesis and what's the chemical equation?"
Study Buddy: "Photosynthesis is the process by which plants convert light energy 
into chemical energy. The equation is: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂"
Sources: biology_textbook.pdf (page 42, relevance: 0.68)
```

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Android App (Kotlin)                │
│                  [In Development 🚧]                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ HTTP/REST API
                       ↓
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │         Document Service                     │   │
│  │  • PDF/DOCX/TXT Processing                  │   │
│  │  • Text Chunking (1000 chars, 200 overlap)  │   │
│  └─────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌─────────────────────────────────────────────┐   │
│  │       Embedding Service                      │   │
│  │  • Sentence Transformers                     │   │
│  │  • 384-dimensional vectors                   │   │
│  │  • Batch processing                          │   │
│  └─────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌─────────────────────────────────────────────┐   │
│  │        Vector Database (ChromaDB)            │   │
│  │  • Semantic search                           │   │
│  │  • Cosine similarity                         │   │
│  │  • Metadata filtering                        │   │
│  └─────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌─────────────────────────────────────────────┐   │
│  │          LLM Service                         │   │
│  │  • Claude Sonnet 4 (Primary)                │   │
│  │  • Gemini 2.0 Flash (Fallback)              │   │
│  │  • Answer generation with sources            │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Features

### ✅ Implemented (Backend)
- 📄 **Multi-format document support** (PDF, DOCX, TXT)
- 🔍 **Semantic search** with 68%+ relevance accuracy
- 🤖 **Dual LLM integration** (Claude Sonnet 4 & Gemini 2.0 Flash)
- ⚡ **Fast retrieval** (<1 second query response time)
- 📊 **Source attribution** with relevance scores
- 🔄 **Batch processing** for efficiency
- ✅ **Comprehensive testing** (95%+ coverage, 70+ tests)
- 🛡️ **Type-safe** with Pydantic validation
- 📝 **RESTful API** with FastAPI

### 🚧 In Progress
- 📱 **Native Android app** (Kotlin)
- 🔐 **User authentication**
- 💾 **Document library management**
- 💬 **Conversation memory**
- 🌙 **Dark mode**
- 🖼️ **Multi-modal support** (images, diagrams)

---

## 🛠️ Tech Stack

### Backend
| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI |
| **Language** | Python 3.13 |
| **AI/ML** | LangChain, Sentence Transformers |
| **Vector DB** | ChromaDB |
| **LLMs** | Claude Sonnet 4, Gemini 2.0 Flash |
| **Validation** | Pydantic |
| **Testing** | pytest, pytest-asyncio |
| **Document Processing** | pypdf, python-docx |

### Frontend (In Development)
| Category | Technology |
|----------|-----------|
| **Platform** | Android |
| **Language** | Kotlin |
| **UI** | Jetpack Compose / XML |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.13+
- pip and virtualenv
- API keys for Claude and/or Gemini

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy
```

2. **Create virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```bash
# API Keys (Required)
GOOGLE_API_KEY=your_google_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here

# LLM Provider (optional - defaults to "gemini")
LLM_PROVIDER=gemini

# App Settings (optional - has defaults)
DEBUG=False
UPLOAD_DIR=./uploads

# Embedding Settings (optional - has defaults)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

5. **Run the backend server**
```bash
# From project root
cd backend
python -m uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

6. **Access API documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_document_service.py -v

# Run with coverage report
pytest --cov=backend.app --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

**Current Test Coverage:** 95%+ ✅

---

## 📁 Project Structure
```
study-buddy/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration & settings
│   │   ├── models.py               # Pydantic data models
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── document_services.py    # Document processing
│   │       ├── embedding_services.py   # Embedding generation
│   │       ├── vector_services.py      # ChromaDB operations
│   │       └── llm_services.py         # LLM integration
│   └── tests/
│       ├── conftest.py             # pytest configuration
│       ├── test_models.py
│       ├── test_config.py
│       ├── test_document_service.py
│       └── test_embedding_service.py
├── android/                         # 🚧 In Development
│   └── app/
│       └── src/
│           └── main/
│               └── kotlin/
├── .env                            # Environment variables (create this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🎮 Usage Example

### Using the API

**1. Upload a document**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@biology_textbook.pdf"
```

Response:
```json
{
  "success": true,
  "message": "File processed successfully",
  "filename": "biology_textbook.pdf",
  "chunks_created": 42,
  "document_id": "doc_abc123"
}
```

**2. Ask a question**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is photosynthesis?",
    "num_contexts": 3
  }'
```

Response:
```json
{
  "answer": "Photosynthesis is the process by which plants...",
  "sources": [
    {
      "document_name": "biology_textbook.pdf",
      "chunk_id": "doc_abc123_chunk_5",
      "relevance_score": 0.84
    }
  ],
  "query_time_seconds": 0.89
}
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Retrieval Accuracy** | 68%+ relevance scores |
| **Query Response Time** | <1 second |
| **Test Coverage** | 95%+ |
| **Embedding Dimension** | 384 |
| **Supported Formats** | PDF, DOCX, TXT |
| **Chunk Size** | 1000 characters |
| **Chunk Overlap** | 200 characters |

---

## 🧠 What I Learned

### Backend Development
- ✅ Building production-ready RAG systems from scratch
- ✅ Vector databases and semantic search
- ✅ Embedding models and similarity calculations
- ✅ LLM API integration with error handling
- ✅ Comprehensive testing strategies for AI systems
- ✅ Type-safe Python with Pydantic
- ✅ Async programming patterns
- ✅ RESTful API design with FastAPI

### In Progress (Android)
- 🚧 Kotlin programming
- 🚧 Jetpack Compose
- 🚧 Mobile app architecture (MVVM)
- 🚧 Retrofit for API calls
- 🚧 Material Design 3

### General Software Engineering
- ✅ The importance of testing (95% coverage saved me multiple times!)
- ✅ Type safety makes debugging easier
- ✅ Good architecture enables fast iteration
- ✅ Documentation is for future you
- ✅ AI is 20% models, 80% engineering

---

## 🐛 Known Issues & Limitations

- 📄 Large PDFs (>50MB) may take longer to process
- 🔍 Similarity search accuracy depends on document quality
- 💰 LLM API costs can add up with heavy usage
- 🌐 Requires internet connection for LLM calls
- 📱 Android app not yet released

---

## 🗺️ Roadmap

### Phase 1: Core Backend ✅ (Complete)
- [x] Document processing pipeline
- [x] Embedding generation
- [x] Vector database integration
- [x] LLM integration
- [x] RESTful API
- [x] Comprehensive testing

### Phase 2: Android Frontend 🚧 (In Progress)
- [ ] UI/UX design
- [ ] Document upload screen
- [ ] Q&A interface
- [ ] Document library
- [ ] Settings & preferences

### Phase 3: Enhanced Features 📋 (Planned)
- [ ] User authentication
- [ ] Conversation history
- [ ] Multi-modal support (images)
- [ ] Offline mode
- [ ] Export answers to notes
- [ ] Study session analytics

### Phase 4: Polish & Deploy 🚀 (Future)
- [ ] Performance optimization
- [ ] Cloud deployment
- [ ] Play Store release
- [ ] User feedback integration

---

## 🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

If you'd like to:
- Report a bug → Open an issue
- Suggest a feature → Open an issue with the "enhancement" label
- Ask a question → Feel free to reach out!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Anthropic** for Claude API
- **Google** for Gemini API
- **LangChain** for document processing tools
- **Sentence Transformers** for embedding models
- **ChromaDB** for the vector database
- **FastAPI** for the amazing web framework

---

## 📧 Contact

**Developer:** Your Name

- LinkedIn: [your-linkedin](https://linkedin.com/in/your-profile)
- GitHub: [your-github](https://github.com/your-username)
- Email: your.email@example.com

---

## 📸 Screenshots

### API Documentation (Swagger UI)
![Swagger UI](screenshots/swagger-ui.png)

### Streamlit Prototype (Development)
![Streamlit Prototype](screenshots/streamlit-demo.png)

### Android App (Coming Soon!)
![Android App](screenshots/android-coming-soon.png)

---

<div align="center">

**Built with ❤️ for learning and fun**

*"The best way to learn is to build."*

⭐ Star this repo if you find it interesting!

</div>