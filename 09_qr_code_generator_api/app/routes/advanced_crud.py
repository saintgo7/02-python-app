from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["advanced-crud"])


class PaginationParams:
    """Pagination parameters"""
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit


def apply_search(query, model, search_fields: List[str], search_term: str):
    """Apply search filtering"""
    if not search_term:
        return query

    search_conditions = [
        getattr(model, field).ilike(f"%{search_term}%")
        for field in search_fields
        if hasattr(model, field)
    ]

    if search_conditions:
        query = query.filter(or_(*search_conditions))

    return query


def apply_sort(query, model, sort_by: str, sort_order: str):
    """Apply sorting"""
    if not sort_by or not hasattr(model, sort_by):
        return query

    column = getattr(model, sort_by)
    if sort_order.lower() == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query


def apply_pagination(query, pagination: PaginationParams):
    """Apply pagination"""
    return query.offset(pagination.skip).limit(pagination.limit)


@router.get("/search")
def advanced_search(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced search with sorting and pagination"""
    query = db.query(models.Item).filter(models.Item.user_id == current_user["user_id"])
    query = apply_search(query, models.Item, ["name", "description"], q)
    query = apply_sort(query, models.Item, sort_by, sort_order)

    total = query.count()
    items = apply_pagination(query, PaginationParams(skip, limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


@router.get("/filter")
def advanced_filter(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced filtering with dynamic conditions"""
    query = db.query(models.Item).filter(models.Item.user_id == current_user["user_id"])

    if is_active is not None:
        query = query.filter(models.Item.is_active == is_active)

    query = apply_sort(query, models.Item, sort_by, sort_order)

    total = query.count()
    items = apply_pagination(query, PaginationParams(skip, limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }
