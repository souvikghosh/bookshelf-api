"""Book routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud
from ..auth import get_current_active_user
from ..database import get_db
from ..models import User
from ..schemas import BookCreate, BookResponse, BookUpdate, PaginatedBooks

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=PaginatedBooks)
def list_books(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = None,
    genre: str | None = None,
    read: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all books with optional filtering and pagination."""
    skip = (page - 1) * per_page
    books, total = crud.get_books(
        db,
        current_user,
        skip=skip,
        limit=per_page,
        search=search,
        genre=genre,
        read=read,
    )
    pages = (total + per_page - 1) // per_page

    return PaginatedBooks(
        items=books,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new book."""
    return crud.create_book(db, book, current_user)


@router.get("/genres", response_model=list[str])
def list_genres(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all unique genres."""
    return crud.get_genres(db, current_user)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get reading statistics."""
    return crud.get_stats(db, current_user)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific book by ID."""
    book = crud.get_book(db, book_id, current_user)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a book."""
    book = crud.update_book(db, book_id, book_update, current_user)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a book."""
    if not crud.delete_book(db, book_id, current_user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
