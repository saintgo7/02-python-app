from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_graphql import GraphQL
from app.core.database import init_db
from app.routes import auth, advanced_crud, websocket
from config import settings
from app.cache import cache
from app.graphql_schema import schema

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="07_api_monitoring_service",
    version="1.0.0",
    description="07_api_monitoring_service API with Advanced Features"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(advanced_crud.router)
app.include_router(websocket.router)

# GraphQL endpoint
app.add_route("/graphql", GraphQL(schema))


@app.get("/")
def read_root():
    return {
        "message": "07_api_monitoring_service API with Advanced Features",
        "version": "1.0.0",
        "features": ["REST API", "Advanced Filtering", "Redis Caching", "WebSocket", "GraphQL"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "cache": "connected" if cache.client else "disconnected"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("🚀 Starting 07_api_monitoring_service with advanced features...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    print("🛑 Shutting down 07_api_monitoring_service...")
    if cache.client:
        cache.client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
