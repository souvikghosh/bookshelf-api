"""Tests for book endpoints."""


class TestCreateBook:
    def test_create_book(self, client, auth_headers):
        response = client.post(
            "/books",
            json={
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "year_published": 1925,
                "genre": "Fiction",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "The Great Gatsby"
        assert data["author"] == "F. Scott Fitzgerald"
        assert "id" in data

    def test_create_book_unauthorized(self, client):
        response = client.post(
            "/books",
            json={"title": "Test", "author": "Author"},
        )
        assert response.status_code == 401

    def test_create_book_minimal(self, client, auth_headers):
        response = client.post(
            "/books",
            json={"title": "Minimal Book", "author": "Author"},
            headers=auth_headers,
        )
        assert response.status_code == 201


class TestListBooks:
    def test_list_books_empty(self, client, auth_headers):
        response = client.get("/books", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_books_with_data(self, client, auth_headers):
        # Create a book
        client.post(
            "/books",
            json={"title": "Book 1", "author": "Author 1"},
            headers=auth_headers,
        )
        client.post(
            "/books",
            json={"title": "Book 2", "author": "Author 2"},
            headers=auth_headers,
        )

        response = client.get("/books", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_list_books_pagination(self, client, auth_headers):
        # Create 5 books
        for i in range(5):
            client.post(
                "/books",
                json={"title": f"Book {i}", "author": f"Author {i}"},
                headers=auth_headers,
            )

        response = client.get("/books?page=1&per_page=2", headers=auth_headers)
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["pages"] == 3

    def test_search_books(self, client, auth_headers):
        client.post(
            "/books",
            json={"title": "Python Programming", "author": "John"},
            headers=auth_headers,
        )
        client.post(
            "/books",
            json={"title": "Java Basics", "author": "Jane"},
            headers=auth_headers,
        )

        response = client.get("/books?search=python", headers=auth_headers)
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Python Programming"

    def test_filter_by_genre(self, client, auth_headers):
        client.post(
            "/books",
            json={"title": "Sci-Fi Book", "author": "A", "genre": "Sci-Fi"},
            headers=auth_headers,
        )
        client.post(
            "/books",
            json={"title": "Fantasy Book", "author": "B", "genre": "Fantasy"},
            headers=auth_headers,
        )

        response = client.get("/books?genre=Sci-Fi", headers=auth_headers)
        data = response.json()
        assert data["total"] == 1


class TestGetBook:
    def test_get_book(self, client, auth_headers):
        # Create a book
        create_resp = client.post(
            "/books",
            json={"title": "Test Book", "author": "Author"},
            headers=auth_headers,
        )
        book_id = create_resp.json()["id"]

        response = client.get(f"/books/{book_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Test Book"

    def test_get_book_not_found(self, client, auth_headers):
        response = client.get("/books/9999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateBook:
    def test_update_book(self, client, auth_headers):
        # Create a book
        create_resp = client.post(
            "/books",
            json={"title": "Original", "author": "Author"},
            headers=auth_headers,
        )
        book_id = create_resp.json()["id"]

        response = client.patch(
            f"/books/{book_id}",
            json={"title": "Updated Title", "read": True, "rating": 5},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["read"] is True
        assert data["rating"] == 5

    def test_update_book_not_found(self, client, auth_headers):
        response = client.patch(
            "/books/9999",
            json={"title": "Updated"},
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestDeleteBook:
    def test_delete_book(self, client, auth_headers):
        # Create a book
        create_resp = client.post(
            "/books",
            json={"title": "To Delete", "author": "Author"},
            headers=auth_headers,
        )
        book_id = create_resp.json()["id"]

        response = client.delete(f"/books/{book_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify it's deleted
        response = client.get(f"/books/{book_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_book_not_found(self, client, auth_headers):
        response = client.delete("/books/9999", headers=auth_headers)
        assert response.status_code == 404


class TestGenresAndStats:
    def test_list_genres(self, client, auth_headers):
        client.post(
            "/books",
            json={"title": "B1", "author": "A", "genre": "Fiction"},
            headers=auth_headers,
        )
        client.post(
            "/books",
            json={"title": "B2", "author": "A", "genre": "Sci-Fi"},
            headers=auth_headers,
        )

        response = client.get("/books/genres", headers=auth_headers)
        assert response.status_code == 200
        genres = response.json()
        assert "Fiction" in genres
        assert "Sci-Fi" in genres

    def test_get_stats(self, client, auth_headers):
        client.post(
            "/books",
            json={"title": "B1", "author": "A", "read": True, "rating": 5},
            headers=auth_headers,
        )
        client.post(
            "/books",
            json={"title": "B2", "author": "A", "read": False},
            headers=auth_headers,
        )

        response = client.get("/books/stats", headers=auth_headers)
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_books"] == 2
        assert stats["books_read"] == 1
        assert stats["books_unread"] == 1
        assert stats["average_rating"] == 5.0
