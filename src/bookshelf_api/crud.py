"""CRUD operations for books."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import Book, User
from .schemas import BookCreate, BookUpdate


def get_books(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    genre: str | None = None,
    read: bool | None = None,
) -> tuple[list[Book], int]:
    """Get books with filtering and pagination."""
    query = db.query(Book).filter(Book.owner_id == user.id)

    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
            )
        )

    if genre:
        query = query.filter(Book.genre == genre)

    if read is not None:
        query = query.filter(Book.read == read)

    total = query.count()
    books = query.order_by(Book.created_at.desc()).offset(skip).limit(limit).all()

    return books, total


def get_book(db: Session, book_id: int, user: User) -> Book | None:
    """Get a single book by ID."""
    return (
        db.query(Book)
        .filter(Book.id == book_id, Book.owner_id == user.id)
        .first()
    )


def create_book(db: Session, book: BookCreate, user: User) -> Book:
    """Create a new book."""
    db_book = Book(**book.model_dump(), owner_id=user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: BookUpdate, user: User) -> Book | None:
    """Update a book."""
    db_book = get_book(db, book_id, user)
    if not db_book:
        return None

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int, user: User) -> bool:
    """Delete a book."""
    db_book = get_book(db, book_id, user)
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()
    return True


def get_genres(db: Session, user: User) -> list[str]:
    """Get all unique genres for a user's books."""
    result = (
        db.query(Book.genre)
        .filter(Book.owner_id == user.id, Book.genre.isnot(None))
        .distinct()
        .all()
    )
    return [r[0] for r in result if r[0]]


def get_stats(db: Session, user: User) -> dict:
    """Get reading statistics for a user."""
    total = db.query(Book).filter(Book.owner_id == user.id).count()
    read = db.query(Book).filter(Book.owner_id == user.id, Book.read == True).count()
    unread = total - read

    avg_rating = None
    rated_books = (
        db.query(Book)
        .filter(Book.owner_id == user.id, Book.rating.isnot(None))
        .all()
    )
    if rated_books:
        avg_rating = sum(b.rating for b in rated_books) / len(rated_books)

    return {
        "total_books": total,
        "books_read": read,
        "books_unread": unread,
        "average_rating": round(avg_rating, 2) if avg_rating else None,
    }
