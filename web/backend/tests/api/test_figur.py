from fastapi import status


def test_create_figur(client, app_token_headers):
    """Test creating a new figur."""
    response = client.post(
        "/api/figur",
        json={
            "name": "Ballettbein",
            "kategorie": "Ballettbein",
            "beschreibung": "Ein Bein gestreckt, ein Bein angewinkelt",
            "schwierigkeitsgrad": 13.0,
            "altersklasse": "U9–U11"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Ballettbein"
    assert data["schwierigkeitsgrad"] == 13.0
    assert "id" in data


def test_read_figur_list(client, app_token_headers):
    """Test reading list of figuren."""
    # Create figur
    client.post(
        "/api/figur",
        json={
            "name": "Vertikale",
            "kategorie": "Vertikale",
            "schwierigkeitsgrad": 16.0
        },
        headers=app_token_headers
    )

    response = client.get("/api/figur", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert any(f["name"] == "Vertikale" for f in data)


def test_read_figur_by_id(client, app_token_headers):
    """Test reading a single figur by ID."""
    # Create
    res = client.post(
        "/api/figur",
        json={
            "name": "Spagat",
            "kategorie": "Spagat",
            "beschreibung": "Beine im 180°-Winkel gespreizt",
            "schwierigkeitsgrad": 14.0
        },
        headers=app_token_headers
    )
    figur_id = res.json()["id"]

    # Read
    response = client.get(f"/api/figur/{figur_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Spagat"
    assert data["schwierigkeitsgrad"] == 14.0


def test_update_figur(client, app_token_headers):
    """Test updating a figur."""
    # Create
    res = client.post(
        "/api/figur",
        json={
            "name": "Old Figur",
            "kategorie": "Test",
            "schwierigkeitsgrad": 10.0
        },
        headers=app_token_headers
    )
    figur_id = res.json()["id"]

    # Update
    response = client.put(
        f"/api/figur/{figur_id}",
        json={
            "name": "Updated Figur",
            "kategorie": "Updated Category",
            "schwierigkeitsgrad": 15.0
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    updated = response.json()
    assert updated["name"] == "Updated Figur"
    assert updated["schwierigkeitsgrad"] == 15.0


def test_delete_figur(client, app_token_headers):
    """Test deleting a figur."""
    # Create
    res = client.post(
        "/api/figur",
        json={
            "name": "To Delete",
            "kategorie": "Test",
            "schwierigkeitsgrad": 12.0
        },
        headers=app_token_headers
    )
    figur_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/figur/{figur_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/figur/{figur_id}", headers=app_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_figur_minimal_fields(client, app_token_headers):
    """Test creating figur with only required fields."""
    response = client.post(
        "/api/figur",
        json={
            "name": "Minimal Figur"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Minimal Figur"
    assert data["kategorie"] is None
    assert data["schwierigkeitsgrad"] is None
