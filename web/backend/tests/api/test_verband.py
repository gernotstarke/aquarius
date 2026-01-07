"""Test API endpoints for Verband (Association) - Read-only."""
from fastapi import status


def test_read_verband_list(client, db):
    """Test getting list of associations."""
    # Verband data comes from seed data, so we just test reading
    response = client.get("/api/verband")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    
    # Check structure of first item if any exist
    if len(data) > 0:
        verband = data[0]
        assert "id" in verband
        assert "name" in verband
        assert "abkuerzung" in verband
        assert "land" in verband
        assert "ort" in verband
        assert "nomination_count" in verband  # Special field with count


def test_read_verband_sorting_by_name(client, db):
    """Test sorting associations by name."""
    response = client.get("/api/verband?sort_by=name&sort_order=asc")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify sorted if we have data
    if len(data) > 1:
        names = [v["name"] for v in data]
        assert names == sorted(names)


def test_read_verband_sorting_by_nomination_count(client, db):
    """Test sorting associations by nomination count."""
    response = client.get("/api/verband?sort_by=nomination_count&sort_order=desc")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify sorted if we have data
    if len(data) > 1:
        counts = [v["nomination_count"] for v in data]
        assert counts == sorted(counts, reverse=True)


def test_read_verband_pagination(client, db):
    """Test pagination for associations."""
    # Get first 5
    response = client.get("/api/verband?limit=5")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) <= 5
    
    # Skip and limit
    response = client.get("/api/verband?skip=2&limit=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) <= 3
