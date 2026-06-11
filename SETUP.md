# Complete Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (recommended)
- PostgreSQL 16 (if not using Docker)
- Git

## Step 1: Clone & Setup Project

```bash
git clone <repository-url>
cd resume-parser-project
```

## Step 2: Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/resume_parser

# JWT Security
SECRET_KEY=generate-a-secure-random-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Providers (Get API keys from respective platforms)
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OLLAMA_BASE_URL=http://localhost:11434

# Application
DEBUG=false
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# File Upload
MAX_UPLOAD_SIZE_MB=10
UPLOAD_DIR=uploads

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_data
```

## Option A: Quick Start with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# First time: Initialize database
docker-compose exec backend alembic upgrade head
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option B: Local Development Setup

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Create .env file
cp ../.env .

# Initialize database
alembic upgrade head

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access frontend at: http://localhost:5173

## Database Setup

### Using PostgreSQL Directly

```bash
# Install PostgreSQL
# Create database
createdb resume_parser

# Create user
createuser -P postgres

# Set environment
export DATABASE_URL=postgresql://postgres:password@localhost:5432/resume_parser

# Run migrations
alembic upgrade head
```

### Using Docker

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_DB=resume_parser \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine
```

## LLM Provider Setup

### Gemini (Google)
1. Visit https://makersuite.google.com/app/apikeys
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=your_key`

### Groq
1. Visit https://console.groq.com
2. Create API key
3. Add to `.env`: `GROQ_API_KEY=your_key`

### Ollama (Local)
1. Download from https://ollama.ai
2. Install and start service
3. Pull models: `ollama pull llama2`
4. Update `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=services --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
```

## API Testing

Use the built-in Swagger UI:
```
http://localhost:8000/docs
```

Or with curl:
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"securepass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'

# Upload resume
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
kill -9 <PID>
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
psql -U postgres -h localhost -d resume_parser

# Verify CONNECTION_STRING in .env
```

### Dependency Issues
```bash
# Clear pip cache
pip install --no-cache-dir -r requirements.txt

# Rebuild Docker images
docker-compose down
docker-compose build --no-cache
```

### CORS Errors
- Check `ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL is listed

## Production Deployment

### Docker Production Build
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### AWS EC2 Deployment
```bash
# SSH into instance
ssh -i key.pem ubuntu@ec2-instance

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and setup
git clone <repo>
cd resume-parser-project
cp .env.example .env

# Edit .env with production values
nano .env

# Start services
docker-compose up -d

# Setup SSL with Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

### Monitoring & Logs
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Monitor resources
docker stats
```

## Next Steps

1. Create user account via signup endpoint
2. Upload a resume (PDF or DOCX)
3. Configure a job description
4. Calculate ATS score
5. View skill gap analysis

## Support & Documentation

- API Documentation: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/swagger
- ReDoc: http://localhost:8000/redoc
