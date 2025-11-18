from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== Form CRUD Operations ==========

@router.get("/forms", response_model=List[schemas.FormResponse])
def get_forms(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all forms with pagination"""
    forms = db.query(models.Form).filter(
        models.Form.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return forms


@router.post("/forms", response_model=schemas.FormResponse, status_code=status.HTTP_201_CREATED)
def create_form(
    form: schemas.FormCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new form"""
    db_form = models.Form(
        **form.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form


@router.get("/forms/{item_id}", response_model=schemas.FormResponse)
def get_form(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific form"""
    form = db.query(models.Form).filter(
        models.Form.id == item_id,
        models.Form.user_id == current_user["user_id"]
    ).first()

    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    return form


@router.put("/forms/{item_id}", response_model=schemas.FormResponse)
def update_form(
    item_id: int,
    form_update: schemas.FormUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update form"""
    db_form = db.query(models.Form).filter(
        models.Form.id == item_id,
        models.Form.user_id == current_user["user_id"]
    ).first()

    if not db_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    update_data = form_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_form, key, value)

    db.commit()
    db.refresh(db_form)
    return db_form


@router.delete("/forms/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_form(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete form"""
    db_form = db.query(models.Form).filter(
        models.Form.id == item_id,
        models.Form.user_id == current_user["user_id"]
    ).first()

    if not db_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    db.delete(db_form)
    db.commit()


# ========== Field CRUD Operations ==========

@router.get("/fields", response_model=List[schemas.FieldResponse])
def get_fields(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all fields with pagination"""
    fields = db.query(models.Field).filter(
        models.Field.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return fields


@router.post("/fields", response_model=schemas.FieldResponse, status_code=status.HTTP_201_CREATED)
def create_field(
    field: schemas.FieldCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new field"""
    db_field = models.Field(
        **field.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


@router.get("/fields/{item_id}", response_model=schemas.FieldResponse)
def get_field(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific field"""
    field = db.query(models.Field).filter(
        models.Field.id == item_id,
        models.Field.user_id == current_user["user_id"]
    ).first()

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )
    return field


@router.put("/fields/{item_id}", response_model=schemas.FieldResponse)
def update_field(
    item_id: int,
    field_update: schemas.FieldUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update field"""
    db_field = db.query(models.Field).filter(
        models.Field.id == item_id,
        models.Field.user_id == current_user["user_id"]
    ).first()

    if not db_field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    update_data = field_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_field, key, value)

    db.commit()
    db.refresh(db_field)
    return db_field


@router.delete("/fields/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_field(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete field"""
    db_field = db.query(models.Field).filter(
        models.Field.id == item_id,
        models.Field.user_id == current_user["user_id"]
    ).first()

    if not db_field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    db.delete(db_field)
    db.commit()


# ========== Submission CRUD Operations ==========

@router.get("/submissions", response_model=List[schemas.SubmissionResponse])
def get_submissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all submissions with pagination"""
    submissions = db.query(models.Submission).filter(
        models.Submission.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return submissions


@router.post("/submissions", response_model=schemas.SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission: schemas.SubmissionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new submission"""
    db_submission = models.Submission(
        **submission.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


@router.get("/submissions/{item_id}", response_model=schemas.SubmissionResponse)
def get_submission(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific submission"""
    submission = db.query(models.Submission).filter(
        models.Submission.id == item_id,
        models.Submission.user_id == current_user["user_id"]
    ).first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    return submission


@router.put("/submissions/{item_id}", response_model=schemas.SubmissionResponse)
def update_submission(
    item_id: int,
    submission_update: schemas.SubmissionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update submission"""
    db_submission = db.query(models.Submission).filter(
        models.Submission.id == item_id,
        models.Submission.user_id == current_user["user_id"]
    ).first()

    if not db_submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    update_data = submission_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_submission, key, value)

    db.commit()
    db.refresh(db_submission)
    return db_submission


@router.delete("/submissions/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete submission"""
    db_submission = db.query(models.Submission).filter(
        models.Submission.id == item_id,
        models.Submission.user_id == current_user["user_id"]
    ).first()

    if not db_submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    db.delete(db_submission)
    db.commit()


