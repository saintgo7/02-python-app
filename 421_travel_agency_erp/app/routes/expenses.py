"""Expense management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Expense, TravelPackage, User, UserRole
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from typing import List

router = APIRouter(prefix="/expenses", tags=["expenses"])


def check_admin(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if user is admin"""
    user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage expenses"
        )
    return user


@router.get("/", response_model=List[ExpenseResponse])
async def list_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    package_id: int = Query(None),
    category: str = Query(None),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    List expenses (admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        package_id: Filter by package ID
        category: Filter by category
        admin: Admin verification
        db: Database session

    Returns:
        List of expenses
    """
    query = db.query(Expense)

    if package_id:
        query = query.filter(Expense.package_id == package_id)

    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))

    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Get expense details (admin only).

    Args:
        expense_id: Expense ID
        admin: Admin verification
        db: Database session

    Returns:
        Expense data

    Raises:
        HTTPException: If expense not found
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Create expense record (admin only).

    Args:
        expense_data: Expense creation data
        admin: Admin verification
        db: Database session

    Returns:
        Created expense

    Raises:
        HTTPException: If package not found
    """
    # Verify package exists
    package = db.query(TravelPackage).filter(
        TravelPackage.id == expense_data.package_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    db_expense = Expense(**expense_data.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Update expense (admin only).

    Args:
        expense_id: Expense ID
        expense_data: Update data
        admin: Admin verification
        db: Database session

    Returns:
        Updated expense

    Raises:
        HTTPException: If expense not found
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Delete expense (admin only).

    Args:
        expense_id: Expense ID
        admin: Admin verification
        db: Database session

    Raises:
        HTTPException: If expense not found
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()


@router.get("/package/{package_id}/summary")
async def get_package_expenses_summary(
    package_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Get expense summary for a package.

    Args:
        package_id: Package ID
        admin: Admin verification
        db: Database session

    Returns:
        Expense summary by category
    """
    expenses = db.query(Expense).filter(Expense.package_id == package_id).all()

    summary = {}
    total = 0

    for expense in expenses:
        if expense.category not in summary:
            summary[expense.category] = 0
        summary[expense.category] += expense.amount
        total += expense.amount

    return {
        "package_id": package_id,
        "total_expenses": total,
        "by_category": summary,
        "expense_count": len(expenses)
    }
