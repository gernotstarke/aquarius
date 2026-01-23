"""Test API endpoints for Verein (Club)."""
from fastapi import status


def test_create_verein(client, app_token_headers):
    """Ensures a new club can be created via the API."""
    response = client.post(
        "/api/verein",
        json={
            "name": "Test Schwimmverein",
            "ort": "Berlin",
            "register_id": "VR-12345",
            "contact": "info@testschwimmverein.de"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Schwimmverein"
    assert data["ort"] == "Berlin"
    assert data["register_id"] == "VR-12345"
    assert data["contact"] == "info@testschwimmverein.de"
    assert "id" in data


def test_read_verein_list(client, app_token_headers):
    """Ensures the API returns a list of all created clubs."""
    # Create first
    client.post(
        "/api/verein",
        json={
            "name": "Verein 1",
            "ort": "Hamburg",
            "register_id": "VR-001",
            "contact": "verein1@test.de"
        },
        headers=app_token_headers
    )
    client.post(
        "/api/verein",
        json={
            "name": "Verein 2",
            "ort": "Munich",
            "register_id": "VR-002",
            "contact": "verein2@test.de"
        },
        headers=app_token_headers
    )

    response = client.get("/api/verein", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    names = [verein["name"] for verein in data]
    assert "Verein 1" in names
    assert "Verein 2" in names


def test_read_verein_by_id(client, app_token_headers):
    """Test getting a specific club by ID."""
    # Create
    res = client.post(
        "/api/verein",
        json={
            "name": "Specific Verein",
            "ort": "Frankfurt",
            "register_id": "VR-999",
            "contact": "specific@test.de"
        },
        headers=app_token_headers
    )
    verein_id = res.json()["id"]

    # Read
    response = client.get(f"/api/verein/{verein_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Specific Verein"
    assert data["ort"] == "Frankfurt"
    assert data["id"] == verein_id


def test_read_verein_not_found(client, app_token_headers):
    """Test getting non-existent club returns 404."""
    response = client.get("/api/verein/99999", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_verein(client, app_token_headers):
    """Test updating a club."""
    # Create
    res = client.post(
        "/api/verein",
        json={
            "name": "Old Verein Name",
            "ort": "Old City",
            "register_id": "VR-OLD",
            "contact": "old@test.de"
        },
        headers=app_token_headers
    )
    verein_id = res.json()["id"]

    # Update
    response = client.put(
        f"/api/verein/{verein_id}",
        json={
            "name": "New Verein Name",
            "ort": "New City",
            "register_id": "VR-NEW",
            "contact": "new@test.de"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Verein Name"
    assert data["ort"] == "New City"
    assert data["register_id"] == "VR-NEW"
    assert data["contact"] == "new@test.de"


def test_delete_verein(client, app_token_headers):
    """Test deleting a club."""
    # Create
    res = client.post(
        "/api/verein",
        json={
            "name": "To Delete",
            "ort": "Deletion City",
            "register_id": "VR-DEL",
            "contact": "delete@test.de"
        },
        headers=app_token_headers
    )
    verein_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/verein/{verein_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/verein/{verein_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_verein_not_found(client, app_token_headers):
    """Test deleting non-existent club returns 404."""
    response = client.delete("/api/verein/99999", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
