# Resume Parser & ATS Scorer

Production-grade AI Resume Parser and ATS Score Analyzer built with FastAPI, React, and advanced NLP.

## Features

✅ **Resume Parsing** - Extract text from PDF/DOCX with OCR support  
✅ **NLP Pipeline** - SpaCy, Sentence Transformers for entity extraction  
✅ **ATS Scoring** - Weighted scoring with skill, experience, projects matching  
✅ **LLM Integration** - Gemini, Groq, and Ollama support  
✅ **RAG Pipeline** - ChromaDB for semantic search and retrieval  
✅ **Skill Gap Analysis** - Match and recommend missing skills  
✅ **Dashboard** - Real-time charts and analytics  
✅ **Docker** - Complete containerization setup  
✅ **CI/CD** - GitHub Actions pipeline  

## Tech Stack

### Backend
- FastAPI + Uvicorn
- SQLAlchemy + AsyncPG
- PostgreSQL
- SpaCy + Sentence Transformers
- ChromaDB
- Pydantic

### Frontend
- React 18 + TypeScript
- Tailwind CSS
- Recharts for visualizations
- Zustand for state management

### AI/ML
- Gemini 2.5 Flash
- Groq (LLaMA 3.3 70B)
- Ollama (Local models)
- sentence-transformers/all-MiniLM-L6-v2

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Using Docker Compose

```bash
# Clone the repo
git clone <repo>
cd resume-parser-project

# Copy environment file
cp .env.example .env

# Update .env with your API keys
# GEMINI_API_KEY=your_key
# GROQ_API_KEY=your_key

# Start all services
docker-compose up --build

# Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Create .env file
cp ../.env.example .env

# Initialize database
alembic upgrade head

# Start server
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
.
├── backend/
│   ├── api/v1/endpoints/      # API routes
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── repositories/          # Data access
│   ├── parsers/               # Document parsing
│   ├── nlp/                   # NLP pipeline
│   ├── llm/                   # LLM providers
│   ├── rag/                   # RAG implementation
│   ├── vector_db/             # ChromaDB setup
│   ├── core/                  # Config, security, logging
│   ├── database/              # DB connection
│   └── main.py                # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API clients
│   │   ├── hooks/             # Custom hooks
│   │   ├── store/             # Zustand store
│   │   └── types/             # TypeScript types
│   └── public/
├── .github/workflows/         # CI/CD
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register user
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token

### Resume
- `POST /resume/upload` - Upload resume
- `GET /resume/{id}` - Get resume
- `POST /resume/parse` - Parse resume
- `GET /resume/history` - Resume history

### ATS
- `POST /ats/score` - Calculate ATS score
- `GET /ats/scores` - Get score history
- `POST /ats/skill-gap` - Analyze skill gap

### Job Descriptions
- `POST /job/upload` - Upload job description
- `GET /job/{id}` - Get job description

## Configuration

See `.env.example` for all configuration options:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Providers
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
OLLAMA_BASE_URL=http://localhost:11434

# File upload
MAX_UPLOAD_SIZE_MB=10
UPLOAD_DIR=uploads
```

## Testing

```bash
# Backend tests
pytest backend/tests/ -v

# Frontend tests
cd frontend
npm test
```

## Deployment

### AWS EC2

```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Clone repo
git clone <repo>
cd resume-parser-project

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Setup environment
cp .env.example .env
# Edit .env with production values

# Start with Docker Compose
docker-compose -f docker-compose.yml up -d

# Setup Nginx reverse proxy (optional)
# Configure SSL with Let's Encrypt
```

### CI/CD with GitHub Actions

Push to `main` branch triggers:
1. Backend tests with pytest
2. Frontend build and lint
3. Docker image build
4. Security scanning with Trivy

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

MIT

## Support

For issues and questions, please open a GitHub issue.
