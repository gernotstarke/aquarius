from datetime import date

import pytest
from fastapi import status

from app import auth, models


@pytest.fixture
def read_only_headers(db, monkeypatch):
    monkeypatch.setattr(auth, "ENABLE_APP_AUTH", True)
    user = models.User(
        username="readonly_user",
        full_name="Read Only User",
        hashed_password=auth.get_password_hash("readonly-password"),
        role="OFFIZIELLER",
        is_active=True,
        is_app_user=True,
        can_read_all=True,
        can_write_all=False,
    )
    db.add(user)
    db.commit()
    token = auth.create_access_token({"sub": user.username})
    return {"Authorization": f"Bearer {token}"}


def test_read_only_user_cannot_modify_kind(client, db, read_only_headers):
    kind = models.Kind(
        vorname="Lena",
        nachname="Fischer",
        geburtsdatum=date(2014, 5, 12),
    )
    db.add(kind)
    db.commit()
    db.refresh(kind)

    create_payload = {
        "vorname": "Mila",
        "nachname": "Schmidt",
        "geburtsdatum": "2015-04-03",
    }
    assert (
        client.post("/api/kind", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {"nachname": "Mueller"}
    assert (
        client.put(
            f"/api/kind/{kind.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/kind/{kind.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )


def test_read_only_user_cannot_modify_verein(client, db, read_only_headers):
    verein = models.Verein(
        name="Start Verein",
        ort="Berlin",
        register_id="VR-101",
        contact="kontakt@verein.de",
    )
    db.add(verein)
    db.commit()
    db.refresh(verein)

    create_payload = {
        "name": "Neuer Verein",
        "ort": "Hamburg",
        "register_id": "VR-102",
        "contact": "neuer@verein.de",
    }
    assert (
        client.post("/api/verein", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {
        "name": "Aktualisiert",
        "ort": "Hamburg",
        "register_id": "VR-102",
        "contact": "update@verein.de",
    }
    assert (
        client.put(
            f"/api/verein/{verein.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/verein/{verein.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )


def test_read_only_user_cannot_modify_saison(client, db, read_only_headers):
    saison = models.Saison(
        name="2024",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31),
    )
    db.add(saison)
    db.commit()
    db.refresh(saison)

    create_payload = {
        "name": "2025",
        "from_date": "2025-01-01",
        "to_date": "2025-12-31",
    }
    assert (
        client.post("/api/saison", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {
        "name": "2024-Updated",
        "from_date": "2024-01-01",
        "to_date": "2024-12-31",
    }
    assert (
        client.put(
            f"/api/saison/{saison.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/saison/{saison.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )


def test_read_only_user_cannot_modify_schwimmbad(client, db, read_only_headers):
    schwimmbad = models.Schwimmbad(
        name="Nordbad",
        adresse="Nordstrasse 1",
    )
    db.add(schwimmbad)
    db.commit()
    db.refresh(schwimmbad)

    create_payload = {
        "name": "Suedbad",
        "adresse": "Suedstrasse 2",
        "phone_no": "040-123456",
        "manager": "Max Mustermann",
    }
    assert (
        client.post("/api/schwimmbad", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {
        "name": "Nordbad Updated",
        "adresse": "Nordstrasse 2",
        "phone_no": "040-654321",
        "manager": "Erika Muster",
    }
    assert (
        client.put(
            f"/api/schwimmbad/{schwimmbad.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/schwimmbad/{schwimmbad.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )


def test_read_only_user_cannot_modify_wettkampf(client, db, read_only_headers):
    saison = models.Saison(
        name="2024",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31),
    )
    schwimmbad = models.Schwimmbad(
        name="Wettkampfbad",
        adresse="Wettkampfweg 1",
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    wettkampf = models.Wettkampf(
        name="Test Wettkampf",
        datum=date(2024, 6, 1),
        max_teilnehmer=50,
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id,
    )
    db.add(wettkampf)
    db.commit()
    db.refresh(wettkampf)

    create_payload = {
        "name": "Neuer Wettkampf",
        "datum": "2024-07-01",
        "max_teilnehmer": 60,
        "saison_id": saison.id,
        "schwimmbad_id": schwimmbad.id,
    }
    assert (
        client.post("/api/wettkampf", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {
        "name": "Aktualisiert",
        "datum": "2024-06-15",
        "max_teilnehmer": 70,
        "saison_id": saison.id,
        "schwimmbad_id": schwimmbad.id,
    }
    assert (
        client.put(
            f"/api/wettkampf/{wettkampf.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/wettkampf/{wettkampf.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )


def test_read_only_user_cannot_modify_anmeldung(client, db, read_only_headers):
    saison = models.Saison(
        name="2024",
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31),
    )
    schwimmbad = models.Schwimmbad(
        name="Anmeldebad",
        adresse="Anmeldeweg 3",
    )
    db.add_all([saison, schwimmbad])
    db.commit()
    db.refresh(saison)
    db.refresh(schwimmbad)

    wettkampf = models.Wettkampf(
        name="Anmeldung Wettkampf",
        datum=date(2024, 8, 1),
        max_teilnehmer=40,
        saison_id=saison.id,
        schwimmbad_id=schwimmbad.id,
    )
    kind = models.Kind(
        vorname="Lena",
        nachname="Fischer",
        geburtsdatum=date(2014, 5, 12),
    )
    db.add_all([wettkampf, kind])
    db.commit()
    db.refresh(wettkampf)
    db.refresh(kind)

    anmeldung = models.Anmeldung(
        kind_id=kind.id,
        wettkampf_id=wettkampf.id,
        status="aktiv",
        vorlaeufig=0,
    )
    db.add(anmeldung)
    db.commit()
    db.refresh(anmeldung)

    create_payload = {
        "kind_id": kind.id,
        "wettkampf_id": wettkampf.id,
        "figur_ids": [],
    }
    assert (
        client.post("/api/anmeldung", json=create_payload, headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )

    update_payload = {
        "status": "abgemeldet",
        "vorlaeufig": 1,
        "figur_ids": [],
    }
    assert (
        client.put(
            f"/api/anmeldung/{anmeldung.id}",
            json=update_payload,
            headers=read_only_headers,
        ).status_code
        == status.HTTP_403_FORBIDDEN
    )

    assert (
        client.delete(f"/api/anmeldung/{anmeldung.id}", headers=read_only_headers).status_code
        == status.HTTP_403_FORBIDDEN
    )
