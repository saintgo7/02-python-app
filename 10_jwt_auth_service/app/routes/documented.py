from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user

router = APIRouter()


# ============================================
# Authentication Endpoints
# ============================================

@router.post("/auth/register", tags=["Authentication"])
async def register(email: str, password: str):
    """
    Register a new user.

    - **email**: User's email address
    - **password**: User's password (minimum 8 characters)

    Returns the created user object with authentication token.
    """
    pass


@router.post("/auth/login", tags=["Authentication"])
async def login(email: str, password: str):
    """
    Login user with credentials.

    - **email**: User's email address
    - **password**: User's password

    Returns JWT access token and refresh token.
    """
    pass


@router.post("/auth/refresh", tags=["Authentication"])
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh JWT access token.

    Requires valid JWT in Authorization header.

    Returns new access token.
    """
    pass


# ============================================
# Item Management Endpoints
# ============================================

@router.get("/items", tags=["Items"], response_model=dict)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items to return"),
    current_user: dict = Depends(get_current_user)
):
    """
    List all items with pagination.

    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return (1-100)

    Returns paginated list of items.
    """
    pass


@router.post("/items", tags=["Items"], status_code=status.HTTP_201_CREATED)
async def create_item(
    name: str,
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new item.

    - **name**: Item name (required)
    - **description**: Item description (optional)

    Returns created item with ID.
    """
    pass


@router.get("/items/{item_id}", tags=["Items"])
async def get_item(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific item by ID.

    - **item_id**: The ID of the item to retrieve

    Returns item details.
    """
    pass


@router.put("/items/{item_id}", tags=["Items"])
async def update_item(
    item_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing item.

    - **item_id**: The ID of the item to update
    - **name**: New item name (optional)
    - **description**: New description (optional)

    Returns updated item.
    """
    pass


@router.delete("/items/{item_id}", tags=["Items"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an item.

    - **item_id**: The ID of the item to delete

    Returns 204 No Content on success.
    """
    pass


# ============================================
# Advanced Search & Filter Endpoints
# ============================================

@router.get("/search", tags=["Search & Filter"])
async def advanced_search(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user)
):
    """
    Advanced search across all items.

    - **q**: Search query string (required)
    - **skip**: Number of results to skip
    - **limit**: Maximum results to return
    - **sort_by**: Field to sort results by
    - **sort_order**: Sort direction (asc/desc)

    Searches across multiple fields including name and description.
    """
    pass


@router.get("/filter", tags=["Search & Filter"])
async def advanced_filter(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    sort_by: str = Query("created_at"),
    current_user: dict = Depends(get_current_user)
):
    """
    Filter items with advanced options.

    - **is_active**: Filter by active status (optional)
    - **skip**: Number of results to skip
    - **limit**: Maximum results to return
    - **sort_by**: Field to sort by

    Returns filtered and sorted items.
    """
    pass


# ============================================
# Health Check Endpoints
# ============================================

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns application health status and connected services.
    """
    pass


@router.get("/status", tags=["Health"])
async def status_check():
    """
    Get application status.

    Returns detailed status information about the API.
    """
    pass
