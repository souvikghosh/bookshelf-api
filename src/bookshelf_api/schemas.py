"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# User schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


# Token schemas
class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data for JWT payload."""

    username: str | None = None


# Book schemas
class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    isbn: str | None = Field(None, max_length=20)
    description: str | None = None
    year_published: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, max_length=100)
    pages: int | None = Field(None, ge=1)
    read: bool = False
    rating: int | None = Field(None, ge=1, le=5)


class BookCreate(BookBase):
    """Schema for creating a book."""

    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional)."""

    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    isbn: str | None = Field(None, max_length=20)
    description: str | None = None
    year_published: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, max_length=100)
    pages: int | None = Field(None, ge=1)
    read: bool | None = None
    rating: int | None = Field(None, ge=1, le=5)


class BookResponse(BookBase):
    """Schema for book response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class PaginatedBooks(BaseModel):
    """Paginated list of books."""

    items: list[BookResponse]
    total: int
    page: int
    per_page: int
    pages: int
