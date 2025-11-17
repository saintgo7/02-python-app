from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VersionBase(BaseModel):
    name: str
    description: Optional[str] = None


class VersionCreate(VersionBase):
    pass


class VersionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class VersionResponse(VersionBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShareBase(BaseModel):
    name: str
    description: Optional[str] = None


class ShareCreate(ShareBase):
    pass


class ShareUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ShareResponse(ShareBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


