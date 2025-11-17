from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== Expense CRUD Operations ==========

@router.get("/expenses", response_model=List[schemas.ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all expenses with pagination"""
    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return expenses


@router.post("/expenses", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new expense"""
    db_expense = models.Expense(
        **expense.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/expenses/{item_id}", response_model=schemas.ExpenseResponse)
def get_expense(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific expense"""
    expense = db.query(models.Expense).filter(
        models.Expense.id == item_id,
        models.Expense.user_id == current_user["user_id"]
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.put("/expenses/{item_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    item_id: int,
    expense_update: schemas.ExpenseUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update expense"""
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == item_id,
        models.Expense.user_id == current_user["user_id"]
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    update_data = expense_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/expenses/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete expense"""
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == item_id,
        models.Expense.user_id == current_user["user_id"]
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(db_expense)
    db.commit()


# ========== Category CRUD Operations ==========

@router.get("/categorys", response_model=List[schemas.CategoryResponse])
def get_categorys(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all categorys with pagination"""
    categorys = db.query(models.Category).filter(
        models.Category.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return categorys


@router.post("/categorys", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    db_category = models.Category(
        **category.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categorys/{item_id}", response_model=schemas.CategoryResponse)
def get_category(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific category"""
    category = db.query(models.Category).filter(
        models.Category.id == item_id,
        models.Category.user_id == current_user["user_id"]
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.put("/categorys/{item_id}", response_model=schemas.CategoryResponse)
def update_category(
    item_id: int,
    category_update: schemas.CategoryUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update category"""
    db_category = db.query(models.Category).filter(
        models.Category.id == item_id,
        models.Category.user_id == current_user["user_id"]
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    update_data = category_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/categorys/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete category"""
    db_category = db.query(models.Category).filter(
        models.Category.id == item_id,
        models.Category.user_id == current_user["user_id"]
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.delete(db_category)
    db.commit()


# ========== Budget CRUD Operations ==========

@router.get("/budgets", response_model=List[schemas.BudgetResponse])
def get_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all budgets with pagination"""
    budgets = db.query(models.Budget).filter(
        models.Budget.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return budgets


@router.post("/budgets", response_model=schemas.BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget: schemas.BudgetCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new budget"""
    db_budget = models.Budget(
        **budget.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.get("/budgets/{item_id}", response_model=schemas.BudgetResponse)
def get_budget(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific budget"""
    budget = db.query(models.Budget).filter(
        models.Budget.id == item_id,
        models.Budget.user_id == current_user["user_id"]
    ).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget


@router.put("/budgets/{item_id}", response_model=schemas.BudgetResponse)
def update_budget(
    item_id: int,
    budget_update: schemas.BudgetUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update budget"""
    db_budget = db.query(models.Budget).filter(
        models.Budget.id == item_id,
        models.Budget.user_id == current_user["user_id"]
    ).first()

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    update_data = budget_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.delete("/budgets/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete budget"""
    db_budget = db.query(models.Budget).filter(
        models.Budget.id == item_id,
        models.Budget.user_id == current_user["user_id"]
    ).first()

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    db.delete(db_budget)
    db.commit()


