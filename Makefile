.PHONY: help install dev test lint format docker-up docker-down migrate

help:
	@echo "Resume Parser & ATS Scorer - Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Start development servers (docker-compose)"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""
	@echo "Database:"
	@echo "  make migrate       - Run database migrations"

install:
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up --build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

test:
	cd backend && pytest tests/ -v

lint:
	flake8 backend/ --max-line-length=120
	cd frontend && npm run lint

format:
	black backend/
	isort backend/
	cd frontend && npx prettier --write src/

migrate:
	cd backend && alembic upgrade head

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/node_modules frontend/dist
	rm -rf backend/.pytest_cache
