from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.routes import auth, crud
from config import settings

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="09_qr_code_generator_api",
    version="1.0.0",
    description="09_qr_code_generator_api API"
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
app.include_router(crud.router)


@app.get("/")
def read_root():
    return {"message": "09_qr_code_generator_api API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
