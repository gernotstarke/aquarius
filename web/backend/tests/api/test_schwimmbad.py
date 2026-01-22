"""Test API endpoints for Schwimmbad (Swimming Pool)."""
from fastapi import status


def test_create_schwimmbad(client, app_token_headers):
    """Test creating a new swimming pool."""
    response = client.post(
        "/api/schwimmbad",
        json={
            "name": "Test Schwimmbad",
            "adresse": "Teststraße 1, 12345 Teststadt",
            "phone_no": "030-12345678",
            "manager": "Max Mustermann"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Schwimmbad"
    assert data["adresse"] == "Teststraße 1, 12345 Teststadt"
    assert "id" in data


def test_create_schwimmbad_minimal(client, app_token_headers):
    """Test creating a swimming pool with only required fields."""
    response = client.post(
        "/api/schwimmbad",
        json={
            "name": "Minimal Pool",
            "adresse": "Minimal Str. 1"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Minimal Pool"
    assert data["phone_no"] is None
    assert data["manager"] is None


def test_read_schwimmbad_list(client, app_token_headers):
    """Test getting list of swimming pools."""
    # Create first
    client.post(
        "/api/schwimmbad",
        json={"name": "Pool 1", "adresse": "Address 1"},
        headers=app_token_headers
    )
    client.post(
        "/api/schwimmbad",
        json={"name": "Pool 2", "adresse": "Address 2"},
        headers=app_token_headers
    )

    response = client.get("/api/schwimmbad", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    names = [pool["name"] for pool in data]
    assert "Pool 1" in names
    assert "Pool 2" in names


def test_read_schwimmbad_by_id(client, app_token_headers):
    """Test getting a specific swimming pool by ID."""
    # Create
    res = client.post(
        "/api/schwimmbad",
        json={"name": "Specific Pool", "adresse": "Specific Address"},
        headers=app_token_headers
    )
    pool_id = res.json()["id"]

    # Read
    response = client.get(f"/api/schwimmbad/{pool_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Specific Pool"
    assert data["id"] == pool_id


def test_read_schwimmbad_not_found(client, app_token_headers):
    """Test getting non-existent swimming pool returns 404."""
    response = client.get("/api/schwimmbad/99999", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_schwimmbad(client, app_token_headers):
    """Test updating a swimming pool."""
    # Create
    res = client.post(
        "/api/schwimmbad",
        json={"name": "Old Name", "adresse": "Old Address"},
        headers=app_token_headers
    )
    pool_id = res.json()["id"]

    # Update
    response = client.put(
        f"/api/schwimmbad/{pool_id}",
        json={
            "name": "New Name",
            "adresse": "New Address",
            "phone_no": "030-99999999",
            "manager": "New Manager"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Name"
    assert data["adresse"] == "New Address"
    assert data["phone_no"] == "030-99999999"
    assert data["manager"] == "New Manager"


def test_delete_schwimmbad(client, app_token_headers):
    """Test deleting a swimming pool."""
    # Create
    res = client.post(
        "/api/schwimmbad",
        json={"name": "To Delete", "adresse": "Delete Address"},
        headers=app_token_headers
    )
    pool_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/schwimmbad/{pool_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/schwimmbad/{pool_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_schwimmbad_not_found(client, app_token_headers):
    """Test deleting non-existent swimming pool returns 404."""
    response = client.delete("/api/schwimmbad/99999", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
