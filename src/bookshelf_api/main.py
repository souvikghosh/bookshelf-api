"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables
from .routes import auth_router, books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    create_tables()
    yield


app = FastAPI(
    title="Bookshelf API",
    description="REST API for managing your personal book collection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(books_router)


@app.get("/", tags=["health"])
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bookshelf-api"}


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
