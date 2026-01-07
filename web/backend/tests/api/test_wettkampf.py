from fastapi import status
from datetime import date
from app import models


def test_create_wettkampf(client, db):
    """Test creating a new wettkampf."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    response = client.post(
        "/api/wettkampf",
        json={
            "name": "Herbstcup 2024",
            "datum": "2024-10-15",
            "max_teilnehmer": 100,
            "saison_id": saison.id,
            "schwimmbad_id": schwimmbad.id
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Herbstcup 2024"
    assert data["max_teilnehmer"] == 100
    assert "id" in data


def test_read_wettkampf_list(client, db):
    """Test reading list of wettkämpfe."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    # Create wettkampf
    client.post(
        "/api/wettkampf",
        json={
            "name": "Wintercup 2024",
            "datum": "2024-12-08",
            "saison_id": saison.id,
            "schwimmbad_id": schwimmbad.id
        }
    )

    response = client.get("/api/wettkampf")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Wintercup 2024"


def test_read_wettkampf_by_id(client, db):
    """Test reading a single wettkampf by ID."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    # Create
    res = client.post(
        "/api/wettkampf",
        json={
            "name": "Sommerfest 2024",
            "datum": "2024-07-10",
            "max_teilnehmer": 80,
            "saison_id": saison.id,
            "schwimmbad_id": schwimmbad.id
        }
    )
    wettkampf_id = res.json()["id"]

    # Read
    response = client.get(f"/api/wettkampf/{wettkampf_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Sommerfest 2024"
    assert data["max_teilnehmer"] == 80


def test_update_wettkampf(client, db):
    """Test updating a wettkampf."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    # Store IDs before using them
    saison_id = saison.id
    schwimmbad_id = schwimmbad.id

    # Create
    res = client.post(
        "/api/wettkampf",
        json={
            "name": "Old Name",
            "datum": "2024-05-01",
            "max_teilnehmer": 50,
            "saison_id": saison_id,
            "schwimmbad_id": schwimmbad_id
        }
    )
    wettkampf_id = res.json()["id"]

    # Update
    response = client.put(
        f"/api/wettkampf/{wettkampf_id}",
        json={
            "name": "New Name",
            "datum": "2024-05-15",
            "max_teilnehmer": 120,
            "saison_id": saison_id,
            "schwimmbad_id": schwimmbad_id
        }
    )
    assert response.status_code == status.HTTP_200_OK
    updated = response.json()
    assert updated["name"] == "New Name"
    assert updated["max_teilnehmer"] == 120


def test_delete_wettkampf(client, db):
    """Test deleting a wettkampf."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    # Create
    res = client.post(
        "/api/wettkampf",
        json={
            "name": "To Delete",
            "datum": "2024-06-01",
            "saison_id": saison.id,
            "schwimmbad_id": schwimmbad.id
        }
    )
    wettkampf_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/wettkampf/{wettkampf_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/wettkampf/{wettkampf_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_wettkampf_details_with_figuren_and_anmeldungen(client, db):
    """Test wettkampf/details endpoint returns figuren and anmeldungen."""
    # Create dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    # Create wettkampf
    res = client.post(
        "/api/wettkampf",
        json={
            "name": "Test Wettkampf",
            "datum": "2024-08-01",
            "saison_id": saison.id,
            "schwimmbad_id": schwimmbad.id
        }
    )
    wettkampf_id = res.json()["id"]

    # Get details
    response = client.get(f"/api/wettkampf/{wettkampf_id}/details")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == wettkampf_id
    assert "figuren" in data
    assert "anmeldungen" in data
    assert isinstance(data["figuren"], list)
    assert isinstance(data["anmeldungen"], list)
