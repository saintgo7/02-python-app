from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from app.api_response import APIResponse
from app.error_handling import error_handler
from app.rate_limiting import rate_limiter

app = FastAPI(
    title="Enhanced Tool API",
    version="2.0.0",
    description="Tool with error handling, rate limiting, and database support"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_middleware(request, call_next):
    """Log all requests"""
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()

    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")

    return response


def get_user_id(api_key: Optional[str] = Query(None)) -> str:
    """Get user ID from API key"""
    return api_key or "anonymous"


@app.post("/process")
@error_handler.handle_exception
def process_data(
    data: Dict[str, Any],
    user_id: str = Depends(get_user_id)
):
    """Process data with rate limiting and error handling"""
    allowed, info = rate_limiter.is_allowed(user_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(info["retry_after"])}
        )

    try:
        # Process data
        result = {
            "input": data,
            "processed_at": datetime.utcnow().isoformat(),
        }

        response = APIResponse.success(
            data=result,
            message="Data processed successfully"
        )

        return response.to_dict()

    except Exception as e:
        error_handler.log_error(e, context="process_data")
        response = APIResponse.error(
            message=str(e),
            code=500
        )
        return response.to_dict()


@app.get("/status")
def get_status():
    """Get API status"""
    return APIResponse.success(
        data={"status": "operational"},
        message="API is operational"
    ).to_dict()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
