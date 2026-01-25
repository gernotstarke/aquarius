"""
BDD Step Definitions for Kind (Child) management.

This is a POC demonstrating pytest-bdd integration with the existing
pytest fixtures (client, db, app_token_headers).
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi import status

from app import models

# Load all scenarios from the feature file
scenarios('../features/kind_verwaltung.feature')


# ============================================
# Shared fixtures for BDD scenarios
# ============================================

@pytest.fixture
def context():
    """Shared context dictionary for passing data between steps."""
    return {}


# ============================================
# Given Steps
# ============================================

@given(parsers.parse('ein Verband "{name}" existiert'))
def verband_existiert(db, context, name):
    """Create a Verband (association) in the database."""
    verband = models.Verband(
        name=name,
        abkuerzung=name[:3].upper(),
        land="Deutschland",
        ort="Berlin",
    )
    db.add(verband)
    db.commit()
    db.refresh(verband)
    context['verband'] = verband
    return verband


@given(parsers.parse('eine Versicherung "{name}" existiert'))
def versicherung_existiert(db, context, name):
    """Create a Versicherung (insurance) in the database."""
    versicherung = models.Versicherung(
        name=name,
        kurz=name[:3].upper(),
        land="Deutschland",
        hauptsitz="Hamburg",
    )
    db.add(versicherung)
    db.commit()
    db.refresh(versicherung)
    context['versicherung'] = versicherung
    return versicherung


@given(parsers.parse('ein Kind "{vorname} {nachname}" existiert bereits'))
def kind_existiert_bereits(client, context, app_token_headers, vorname, nachname):
    """Create a Kind via API (assumes Verband and Versicherung exist)."""
    payload = {
        "vorname": vorname,
        "nachname": nachname,
        "geburtsdatum": "2013-03-15",
        "geschlecht": "W",
        "verband_id": context['verband'].id,
        "versicherung_id": context['versicherung'].id,
        "vertrag": f"V-{vorname[:2]}-001",
    }
    response = client.post("/api/kind", json=payload, headers=app_token_headers)
    assert response.status_code == status.HTTP_201_CREATED

    if 'kinder' not in context:
        context['kinder'] = []
    context['kinder'].append(response.json())


# ============================================
# When Steps
# ============================================

@when(parsers.parse('ich ein Kind "{vorname} {nachname}" mit Geburtsdatum "{geburtsdatum}" anlege'))
def kind_anlegen(client, context, app_token_headers, vorname, nachname, geburtsdatum):
    """Create a new Kind via the API."""
    payload = {
        "vorname": vorname,
        "nachname": nachname,
        "geburtsdatum": geburtsdatum,
        "geschlecht": "M",
        "verband_id": context['verband'].id,
        "versicherung_id": context['versicherung'].id,
        "vertrag": f"V-{vorname[:2]}-001",
    }
    response = client.post("/api/kind", json=payload, headers=app_token_headers)
    context['response'] = response
    context['created_kind'] = response.json() if response.status_code == status.HTTP_201_CREATED else None


@when('ich die Liste aller Kinder abrufe')
def liste_kinder_abrufen(client, context, app_token_headers):
    """Fetch the list of all Kinder via API."""
    response = client.get("/api/kind", headers=app_token_headers)
    context['response'] = response
    context['kinder_liste'] = response.json() if response.status_code == status.HTTP_200_OK else []


# ============================================
# Then Steps
# ============================================

@then(parsers.parse('sollte das Kind "{vorname} {nachname}" im System existieren'))
def kind_existiert(context, vorname, nachname):
    """Verify the Kind was created successfully."""
    assert context['response'].status_code == status.HTTP_201_CREATED
    kind = context['created_kind']
    assert kind is not None
    assert kind['vorname'] == vorname
    assert kind['nachname'] == nachname


@then(parsers.parse('das Kind sollte dem Verband "{verband_name}" zugeordnet sein'))
def kind_hat_verband(context, verband_name):
    """Verify the Kind is associated with the correct Verband."""
    kind = context['created_kind']
    assert kind['verband_id'] == context['verband'].id


@then(parsers.parse('sollten mindestens {anzahl:d} Kinder in der Liste sein'))
def mindestens_n_kinder(context, anzahl):
    """Verify at least N children are in the list."""
    assert context['response'].status_code == status.HTTP_200_OK
    assert len(context['kinder_liste']) >= anzahl
