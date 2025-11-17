from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import logging
from app.openapi_config import setup_openapi_documentation
from app.core.database import init_db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="API Documentation",
    version="1.0.0",
    description="Comprehensive REST API with Advanced Features"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup OpenAPI documentation
setup_openapi_documentation(app, "API Documentation", "1.0.0")

# Include routers
from app.routes import auth, items

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(items.router, prefix="/items", tags=["items"])

# Static documentation
docs_dir = Path(__file__).parent.parent / "docs"
if docs_dir.exists():
    try:
        app.mount("/documentation", StaticFiles(directory=docs_dir), name="documentation")
    except:
        pass


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to API Documentation",
        "version": "1.0.0",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "documentation": "/documentation"
        }
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
