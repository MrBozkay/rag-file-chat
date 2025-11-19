# RAG File Chat

A modern, full-stack RAG (Retrieval-Augmented Generation) application that enables intelligent conversations with your documents using Google's Gemini AI.

## 🚀 Features

- **Document Upload & Processing**: Upload various file formats and process them for AI-powered chat
- **AI-Powered Chat**: Engage in intelligent conversations about your documents using Google Gemini
- **Modern UI**: Built with Next.js 14 and Tailwind CSS for a premium user experience
- **RESTful API**: FastAPI backend with async support and comprehensive error handling
- **Database Integration**: SQLAlchemy with SQLite for efficient data management
- **Comprehensive Testing**: Full test suite with pytest

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Google Generative AI**: Gemini AI integration for intelligent responses
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Pytest**: Testing framework with async support

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Axios**: Promise-based HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- Google Gemini API Key

## 🔧 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd rag_file_chat
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./rag_chat.db
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=.txt,.pdf,.doc,.docx
EOF
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Using the start script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This will start both backend (port 8000) and frontend (port 3000) concurrently.

### Manual startup

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=. --cov-report=html  # With coverage report
```

## 📁 Project Structure

```
rag_file_chat/
├── backend/
│   ├── api/              # API routes
│   ├── tests/            # Test suite
│   ├── uploads/          # File upload directory
│   ├── config.py         # Configuration management
│   ├── database.py       # Database setup
│   ├── exceptions.py     # Custom exceptions
│   ├── gemini_client.py  # Gemini AI integration
│   ├── logger.py         # Logging configuration
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utility functions
│   └── package.json      # Node dependencies
├── .gitignore
├── README.md
└── start.sh              # Startup script
```

## 🔑 Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `DATABASE_URL` | Database connection URL | `sqlite+aiosqlite:///./rag_chat.db` |
| `UPLOAD_DIR` | File upload directory | `uploads` |
| `MAX_FILE_SIZE` | Maximum file size in bytes | `10485760` (10MB) |
| `ALLOWED_EXTENSIONS` | Allowed file extensions | `.txt,.pdf,.doc,.docx` |

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language models
- FastAPI for the excellent web framework
- Next.js team for the amazing React framework
