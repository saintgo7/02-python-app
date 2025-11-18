"""User business logic service"""

from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.core.security import hash_password, verify_password
from app.schemas import UserCreate
from fastapi import HTTPException, status


class UserService:
    """Service for user operations"""

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create new user"""
        # Check email uniqueness
        if UserService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check username uniqueness
        if UserService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        return user

    @staticmethod
    def get_guides(db: Session, skip: int = 0, limit: int = 10):
        """Get all active guides"""
        return db.query(User).filter(
            User.role == UserRole.GUIDE,
            User.is_active == True
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_staff(db: Session):
        """Get all staff members"""
        return db.query(User).filter(
            User.role.in_([UserRole.ADMIN, UserRole.STAFF]),
            User.is_active == True
        ).all()

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> User:
        """Deactivate user account"""
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = False
        db.commit()
        db.refresh(user)

        return user
