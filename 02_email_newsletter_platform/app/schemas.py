from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubscriberBase(BaseModel):
    name: str
    description: Optional[str] = None


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SubscriberResponse(SubscriberBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailBase(BaseModel):
    name: str
    description: Optional[str] = None


class EmailCreate(EmailBase):
    pass


class EmailUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class EmailResponse(EmailBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


