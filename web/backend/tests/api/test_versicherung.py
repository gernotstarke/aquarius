"""Test API endpoints for Versicherung (Insurance) - Read-only."""
from fastapi import status


def test_read_versicherung_list(client, db):
    """Test getting list of insurance companies."""
    # Versicherung data comes from seed data, so we just test reading
    response = client.get("/api/versicherung")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    
    # Check structure of first item if any exist
    if len(data) > 0:
        versicherung = data[0]
        assert "id" in versicherung
        assert "name" in versicherung
        assert "kurz" in versicherung
        assert "land" in versicherung
        assert "hauptsitz" in versicherung


def test_read_versicherung_sorted_by_name(client, db):
    """Test that insurance companies are sorted by name."""
    response = client.get("/api/versicherung")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify sorted if we have data (endpoint sorts by name)
    if len(data) > 1:
        names = [v["name"] for v in data]
        assert names == sorted(names)


def test_read_versicherung_pagination(client, db):
    """Test pagination for insurance companies."""
    # Get first 5
    response = client.get("/api/versicherung?limit=5")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) <= 5
    
    # Skip and limit
    response = client.get("/api/versicherung?skip=2&limit=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) <= 3


def test_read_versicherung_default_limit(client, db):
    """Test default limit for insurance companies."""
    # Default limit is 200 according to the endpoint
    response = client.get("/api/versicherung")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Should not exceed default limit
    assert len(data) <= 200
