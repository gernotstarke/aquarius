from fastapi import status

from app import models


def test_kind_crud(client, db):
    verband = models.Verband(
        name="Bezirk Nord",
        abkuerzung="BEN",
        land="Deutschland",
        ort="Kassel",
    )
    versicherung = models.Versicherung(
        name="SchutzSchwarm",
        kurz="SSW",
        land="Deutschland",
        hauptsitz="Hamburg",
    )
    db.add_all([verband, versicherung])
    db.commit()
    db.refresh(verband)
    db.refresh(versicherung)

    create_payload = {
        "vorname": "Lena",
        "nachname": "Fischer",
        "geburtsdatum": "2014-05-12",
        "geschlecht": "W",
        "verband_id": verband.id,
        "versicherung_id": versicherung.id,
        "vertrag": "SSW-2024-0001",
    }
    create_response = client.post("/api/kind", json=create_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    kind_id = created["id"]
    assert created["vorname"] == create_payload["vorname"]
    assert created["nachname"] == create_payload["nachname"]
    assert created["verband_id"] == verband.id
    assert created["versicherung_id"] == create_payload["versicherung_id"]
    assert created["vertrag"] == create_payload["vertrag"]

    get_response = client.get(f"/api/kind/{kind_id}")
    assert get_response.status_code == status.HTTP_200_OK
    fetched = get_response.json()
    assert fetched["id"] == kind_id
    assert fetched["versicherung_id"] == create_payload["versicherung_id"]

    update_payload = {
        "vorname": "Lena",
        "nachname": "Mueller",
        "geburtsdatum": "2014-05-12",
        "geschlecht": "W",
        "verband_id": verband.id,
        "versicherung_id": versicherung.id,
        "vertrag": "SSW-2024-0099",
    }
    update_response = client.put(f"/api/kind/{kind_id}", json=update_payload)
    assert update_response.status_code == status.HTTP_200_OK
    updated = update_response.json()
    assert updated["nachname"] == update_payload["nachname"]
    assert updated["versicherung_id"] == update_payload["versicherung_id"]
    assert updated["vertrag"] == update_payload["vertrag"]

    delete_response = client.delete(f"/api/kind/{kind_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/api/kind/{kind_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    print("testing CRUD for Kind: ok")
