# Bookshelf API

A REST API for managing your personal book collection, built with FastAPI and SQLite.

## Features

- User authentication with JWT tokens
- Full CRUD operations for books
- Search books by title or author
- Filter by genre or read status
- Pagination support
- Reading statistics
- API documentation with Swagger UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/souvikghosh/bookshelf-api.git
cd bookshelf-api
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Run the server:
```bash
uvicorn src.bookshelf_api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get access token |

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books` | List all books (paginated) |
| POST | `/books` | Create a new book |
| GET | `/books/{id}` | Get a specific book |
| PATCH | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
| GET | `/books/genres` | List all genres |
| GET | `/books/stats` | Get reading statistics |

### Query Parameters for GET /books
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)
- `search` - Search in title and author
- `genre` - Filter by genre
- `read` - Filter by read status (true/false)

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "myuser", "password": "securepass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=myuser&password=securepass123"
```

### Add a book
```bash
curl -X POST http://localhost:8000/books \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year_published": 1925,
    "genre": "Fiction",
    "pages": 180
  }'
```

### Search books
```bash
curl "http://localhost:8000/books?search=gatsby" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Mark a book as read with rating
```bash
curl -X PATCH http://localhost:8000/books/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"read": true, "rating": 5}'
```

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest

# Run with coverage
pytest --cov=src/bookshelf_api
```

## Project Structure

```
bookshelf-api/
├── src/
│   └── bookshelf_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI app
│       ├── config.py        # Settings
│       ├── database.py      # Database setup
│       ├── models.py        # SQLAlchemy models
│       ├── schemas.py       # Pydantic schemas
│       ├── auth.py          # Authentication
│       ├── crud.py          # Database operations
│       └── routes/
│           ├── __init__.py
│           ├── auth.py      # Auth endpoints
│           └── books.py     # Book endpoints
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_books.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Technologies

- **FastAPI** - Modern web framework for APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **python-jose** - JWT tokens
- **passlib** - Password hashing
- **pytest** - Testing framework

## License

MIT
