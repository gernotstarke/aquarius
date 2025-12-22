from fastapi import status

def test_create_saison(client):
    response = client.post(
        "/api/saison",
        json={"name": "Test Saison", "from_date": "2024-01-01", "to_date": "2024-12-31"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Saison"
    assert "id" in data

def test_read_saison(client):
    # Create first
    client.post(
        "/api/saison",
        json={"name": "Test Saison", "from_date": "2024-01-01", "to_date": "2024-12-31"}
    )
    
    response = client.get("/api/saison")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Saison"

def test_update_saison(client):
    # Create
    res = client.post(
        "/api/saison",
        json={"name": "Old Name", "from_date": "2024-01-01", "to_date": "2024-12-31"}
    )
    saison_id = res.json()["id"]

    # Update
    response = client.put(
        f"/api/saison/{saison_id}",
        json={"name": "New Name", "from_date": "2024-01-01", "to_date": "2024-12-31"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "New Name"

def test_delete_saison(client):
    # Create
    res = client.post(
        "/api/saison",
        json={"name": "To Delete", "from_date": "2024-01-01", "to_date": "2024-12-31"}
    )
    saison_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/saison/{saison_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/saison/{saison_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
