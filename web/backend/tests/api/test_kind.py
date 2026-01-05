from fastapi import status

from app import models


def test_kind_crud(client, db):
    verband = models.Verband(
        name="Bezirk Nord",
        land="Deutschland",
        ort="Kassel",
    )
    db.add(verband)
    db.commit()
    db.refresh(verband)

    create_payload = {
        "vorname": "Lena",
        "nachname": "Fischer",
        "geburtsdatum": "2014-05-12",
        "geschlecht": "W",
        "verband_id": verband.id,
        "versicherung": "KinderSafe",
        "vertrag": "KS-2024-0001",
    }
    create_response = client.post("/api/kind", json=create_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    kind_id = created["id"]
    assert created["vorname"] == create_payload["vorname"]
    assert created["nachname"] == create_payload["nachname"]
    assert created["verband_id"] == verband.id
    assert created["versicherung"] == create_payload["versicherung"]
    assert created["vertrag"] == create_payload["vertrag"]

    get_response = client.get(f"/api/kind/{kind_id}")
    assert get_response.status_code == status.HTTP_200_OK
    fetched = get_response.json()
    assert fetched["id"] == kind_id
    assert fetched["versicherung"] == create_payload["versicherung"]

    update_payload = {
        "vorname": "Lena",
        "nachname": "Mueller",
        "geburtsdatum": "2014-05-12",
        "geschlecht": "W",
        "verband_id": verband.id,
        "versicherung": "AquaShield",
        "vertrag": "AS-2024-0099",
    }
    update_response = client.put(f"/api/kind/{kind_id}", json=update_payload)
    assert update_response.status_code == status.HTTP_200_OK
    updated = update_response.json()
    assert updated["nachname"] == update_payload["nachname"]
    assert updated["versicherung"] == update_payload["versicherung"]
    assert updated["vertrag"] == update_payload["vertrag"]

    delete_response = client.delete(f"/api/kind/{kind_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/api/kind/{kind_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    print("testing CRUD for Kind: ok")
