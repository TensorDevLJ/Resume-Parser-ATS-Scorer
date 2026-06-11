
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from core.logging import get_logger
from database import init_db
from api.v1.endpoints import auth

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(
    title=settings.app_name,
    description="Production-grade Resume Parser & ATS Scorer",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}

@app.get("/")
async def root():
    return {"message": "Resume Parser & ATS Scorer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
