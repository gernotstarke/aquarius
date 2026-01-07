from datetime import date
from fastapi import status
from app import models


def test_create_anmeldung_with_figuren(client, db):
    """Test creating anmeldung with figures."""
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
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    # Store IDs before using them
    saison_id = saison.id
    schwimmbad_id = schwimmbad.id
    verein_id = verein.id

    # Create wettkampf
    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison_id,
        schwimmbad_id=schwimmbad_id,
        max_teilnehmer=100
    )
    db.add(wettkampf)
    db.commit()
    db.refresh(wettkampf)
    wettkampf_id = wettkampf.id

    # Create kind with verein (insured)
    kind = models.Kind(
        vorname="Max",
        nachname="Mustermann",
        geburtsdatum=date(2014, 5, 12),
        geschlecht="M",
        verein_id=verein_id
    )
    db.add(kind)
    db.commit()
    db.refresh(kind)
    kind_id = kind.id

    # Create figuren
    figur1 = models.Figur(name="Ballettbein", schwierigkeitsgrad=13.0)
    figur2 = models.Figur(name="Vertikale", schwierigkeitsgrad=16.0)
    db.add_all([figur1, figur2])
    db.commit()
    db.refresh(figur1)
    db.refresh(figur2)
    figur1_id = figur1.id
    figur2_id = figur2.id

    # Add figuren to wettkampf
    wettkampf.figuren.extend([figur1, figur2])
    db.commit()

    # Create anmeldung
    response = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind_id,
            "wettkampf_id": wettkampf_id,
            "figur_ids": [figur1_id, figur2_id]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["kind_id"] == kind_id
    assert data["wettkampf_id"] == wettkampf_id
    assert data["vorlaeufig"] == 0  # Should be final (has figures + insured)
    assert data["status"] == "aktiv"
    assert len(data["figuren"]) == 2
    assert data["startnummer"] is not None


def test_create_anmeldung_without_figuren_is_vorlaeufig(client, db):
    """Test anmeldung without figures is marked as preliminary."""
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
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    db.add(wettkampf)
    db.commit()
    db.refresh(wettkampf)

    kind = models.Kind(
        vorname="Anna",
        nachname="Test",
        geburtsdatum=date(2015, 3, 20),
        geschlecht="W",
        verein_id=verein.id
    )
    db.add(kind)
    db.commit()
    db.refresh(kind)

    # Create anmeldung without figuren
    response = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind.id,
            "wettkampf_id": wettkampf.id,
            "figur_ids": []
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["vorlaeufig"] == 1  # Should be preliminary (no figures)


def test_create_anmeldung_uninsured_kind_is_vorlaeufig(client, db):
    """Test anmeldung for uninsured kind is marked as preliminary."""
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

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    db.add(wettkampf)
    db.commit()
    db.refresh(wettkampf)

    # Create kind without insurance (no verein, verband, or versicherung)
    kind = models.Kind(
        vorname="Lena",
        nachname="Unversichert",
        geburtsdatum=date(2016, 7, 10),
        geschlecht="W"
    )
    db.add(kind)
    db.commit()
    db.refresh(kind)

    # Create figur
    figur = models.Figur(name="Spagat", schwierigkeitsgrad=14.0)
    db.add(figur)
    db.commit()
    db.refresh(figur)

    wettkampf.figuren.append(figur)
    db.commit()

    # Create anmeldung
    response = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind.id,
            "wettkampf_id": wettkampf.id,
            "figur_ids": [figur.id]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["vorlaeufig"] == 1  # Should be preliminary (uninsured)
    assert data["insurance_ok"] == False


def test_read_anmeldung_list(client, db):
    """Test reading list of anmeldungen."""
    # Create minimal dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    kind = models.Kind(
        vorname="Test",
        nachname="Kind",
        geburtsdatum=date(2015, 1, 1),
        verein_id=verein.id
    )
    db.add_all([wettkampf, kind])
    db.commit()
    db.refresh(wettkampf)
    db.refresh(kind)

    # Create anmeldung
    client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind.id,
            "wettkampf_id": wettkampf.id,
            "figur_ids": []
        }
    )

    response = client.get("/api/anmeldung")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_read_anmeldung_by_id(client, db):
    """Test reading single anmeldung by ID."""
    # Create minimal dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    kind = models.Kind(
        vorname="Test",
        nachname="Kind",
        geburtsdatum=date(2015, 1, 1),
        verein_id=verein.id
    )
    db.add_all([wettkampf, kind])
    db.commit()
    db.refresh(wettkampf)
    db.refresh(kind)

    # Create
    res = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind.id,
            "wettkampf_id": wettkampf.id,
            "figur_ids": []
        }
    )
    anmeldung_id = res.json()["id"]

    # Read
    response = client.get(f"/api/anmeldung/{anmeldung_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == anmeldung_id
    assert data["kind_id"] == kind.id


def test_update_anmeldung_figuren(client, db):
    """Test updating anmeldung figures."""
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
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    # Store IDs
    saison_id = saison.id
    schwimmbad_id = schwimmbad.id
    verein_id = verein.id

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison_id,
        schwimmbad_id=schwimmbad_id
    )
    kind = models.Kind(
        vorname="Test",
        nachname="Kind",
        geburtsdatum=date(2015, 1, 1),
        verein_id=verein_id
    )
    figur = models.Figur(name="Test Figur", schwierigkeitsgrad=12.0)
    db.add_all([wettkampf, kind, figur])
    db.commit()
    db.refresh(wettkampf)
    db.refresh(kind)
    db.refresh(figur)

    # Store IDs
    wettkampf_id = wettkampf.id
    kind_id = kind.id
    figur_id = figur.id

    wettkampf.figuren.append(figur)
    db.commit()

    # Create anmeldung without figuren
    res = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind_id,
            "wettkampf_id": wettkampf_id,
            "figur_ids": []
        }
    )
    anmeldung_id = res.json()["id"]
    assert res.json()["vorlaeufig"] == 1

    # Update with figuren
    response = client.put(
        f"/api/anmeldung/{anmeldung_id}",
        json={
            "figur_ids": [figur_id]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    updated = response.json()
    assert len(updated["figuren"]) == 1
    # Should now be final (has figures + insured)
    assert updated["vorlaeufig"] == 0


def test_delete_anmeldung(client, db):
    """Test deleting anmeldung."""
    # Create minimal dependencies
    saison = models.Saison(
        name="Test Saison",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31)
    )
    schwimmbad = models.Schwimmbad(
        name="Test Bad",
        adresse="Teststraße 1"
    )
    verein = models.Verein(
        name="Test Verein",
        ort="Berlin",
        register_id="VR12345",
        contact="test@verein.de"
    )
    db.add_all([saison, schwimmbad, verein])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)
    db.refresh(verein)

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    kind = models.Kind(
        vorname="Test",
        nachname="Kind",
        geburtsdatum=date(2015, 1, 1),
        verein_id=verein.id
    )
    db.add_all([wettkampf, kind])
    db.commit()
    db.refresh(wettkampf)
    db.refresh(kind)

    # Create
    res = client.post(
        "/api/anmeldung",
        json={
            "kind_id": kind.id,
            "wettkampf_id": wettkampf.id,
            "figur_ids": []
        }
    )
    anmeldung_id = res.json()["id"]

    # Delete
    response = client.delete(f"/api/anmeldung/{anmeldung_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify gone
    response = client.get(f"/api/anmeldung/{anmeldung_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_anmeldung_kind_not_found(client, db):
    """Test creating anmeldung with non-existent kind returns 404."""
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

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 10, 15),
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id
    )
    db.add(wettkampf)
    db.commit()
    db.refresh(wettkampf)

    response = client.post(
        "/api/anmeldung",
        json={
            "kind_id": 99999,  # Non-existent
            "wettkampf_id": wettkampf.id,
            "figur_ids": []
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Kind not found" in response.json()["detail"]


def test_create_anmeldung_wettkampf_not_found(client):
    """Test creating anmeldung with non-existent wettkampf returns 404."""
    response = client.post(
        "/api/anmeldung",
        json={
            "kind_id": 1,
            "wettkampf_id": 99999,  # Non-existent
            "figur_ids": []
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Wettkampf not found" in response.json()["detail"]
