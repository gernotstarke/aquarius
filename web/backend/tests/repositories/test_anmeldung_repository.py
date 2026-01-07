"""Integration tests for AnmeldungRepository (Step 4)."""
import pytest
from datetime import date
from sqlalchemy.orm import Session

from app.anmeldung.repository import AnmeldungRepository
from app.anmeldung import schemas as anmeldung_schemas
from app import models


def test_anmeldung_repository_get_with_details(db: Session):
    """
    Requirement for Step 4:
    Repo should handle eager loading (joinedload) of 'kind' and 'figuren'.
    """
    # Arrange
    repo = AnmeldungRepository(db)

    # Create supporting data
    kind = models.Kind(
        vorname="Test",
        nachname="Child",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    db.add(kind)

    saison = models.Saison(
        name="2025",
        from_date=date(2025, 1, 1),
        to_date=date(2025, 12, 31)
    )
    db.add(saison)

    schwimmbad = models.Schwimmbad(
        name="Test Pool",
        adresse="Test Address",
        phone_no="123456",
        manager="Test Manager"
    )
    db.add(schwimmbad)

    wettkampf = models.Wettkampf(
        name="Test Competition",
        datum=date(2025, 6, 15),
        saison=saison,
        schwimmbad=schwimmbad
    )
    db.add(wettkampf)

    figur1 = models.Figur(
        name="Figur 1",
        kategorie="Test",
        schwierigkeitsgrad=5
    )
    figur2 = models.Figur(
        name="Figur 2",
        kategorie="Test",
        schwierigkeitsgrad=6
    )
    db.add(figur1)
    db.add(figur2)
    db.commit()

    # Create Anmeldung
    anmeldung = models.Anmeldung(
        kind_id=kind.id,
        wettkampf_id=wettkampf.id,
        startnummer=1,
        anmeldedatum=date.today(),
        vorlaeufig=0,
        status="aktiv"
    )
    anmeldung.figuren.append(figur1)
    anmeldung.figuren.append(figur2)
    db.add(anmeldung)
    db.commit()

    # Act
    result = repo.get_with_details(anmeldung.id)

    # Assert
    assert result is not None
    assert result.kind is not None
    assert result.kind.vorname == "Test"
    assert result.kind.nachname == "Child"
    assert result.figuren is not None
    assert len(result.figuren) == 2
    assert result.figuren[0].name in ["Figur 1", "Figur 2"]


def test_anmeldung_repository_get_next_startnummer(db: Session):
    """
    Requirement for Step 4:
    Repo should assume responsibility for calculating the next startnummer
    (atomic MAX query).
    """
    # Arrange
    repo = AnmeldungRepository(db)

    # Create supporting data
    saison = models.Saison(
        name="2025",
        from_date=date(2025, 1, 1),
        to_date=date(2025, 12, 31)
    )
    db.add(saison)

    schwimmbad = models.Schwimmbad(
        name="Test Pool",
        adresse="Test Address",
        phone_no="123456",
        manager="Test Manager"
    )
    db.add(schwimmbad)

    wettkampf = models.Wettkampf(
        name="Test Competition",
        datum=date(2025, 6, 15),
        saison=saison,
        schwimmbad=schwimmbad
    )
    db.add(wettkampf)
    db.commit()

    # Act - First startnummer should be 1
    next_nr_1 = repo.get_next_startnummer(wettkampf_id=wettkampf.id)

    # Assert
    assert next_nr_1 == 1

    # Arrange - Create an anmeldung with startnummer 1
    kind1 = models.Kind(
        vorname="First",
        nachname="Child",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    db.add(kind1)
    db.commit()

    anmeldung1 = models.Anmeldung(
        kind_id=kind1.id,
        wettkampf_id=wettkampf.id,
        startnummer=1,
        anmeldedatum=date.today(),
        vorlaeufig=0,
        status="aktiv"
    )
    db.add(anmeldung1)
    db.commit()

    # Act - Next startnummer should be 2
    next_nr_2 = repo.get_next_startnummer(wettkampf_id=wettkampf.id)

    # Assert
    assert next_nr_2 == 2

    # Arrange - Create another anmeldung with startnummer 5 (gap)
    kind2 = models.Kind(
        vorname="Second",
        nachname="Child",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="W"
    )
    db.add(kind2)
    db.commit()

    anmeldung2 = models.Anmeldung(
        kind_id=kind2.id,
        wettkampf_id=wettkampf.id,
        startnummer=5,
        anmeldedatum=date.today(),
        vorlaeufig=0,
        status="aktiv"
    )
    db.add(anmeldung2)
    db.commit()

    # Act - Next startnummer should be 6 (max + 1, not filling gaps)
    next_nr_3 = repo.get_next_startnummer(wettkampf_id=wettkampf.id)

    # Assert
    assert next_nr_3 == 6


def test_anmeldung_repository_add_and_set_figuren(db: Session):
    """Test adding and setting figuren for an anmeldung."""
    # Arrange
    repo = AnmeldungRepository(db)

    # Create supporting data
    kind = models.Kind(
        vorname="Test",
        nachname="Child",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    db.add(kind)

    saison = models.Saison(
        name="2025",
        from_date=date(2025, 1, 1),
        to_date=date(2025, 12, 31)
    )
    db.add(saison)

    schwimmbad = models.Schwimmbad(
        name="Test Pool",
        adresse="Test Address",
        phone_no="123456",
        manager="Test Manager"
    )
    db.add(schwimmbad)

    wettkampf = models.Wettkampf(
        name="Test Competition",
        datum=date(2025, 6, 15),
        saison=saison,
        schwimmbad=schwimmbad
    )
    db.add(wettkampf)

    figur1 = models.Figur(name="F1", kategorie="Test", schwierigkeitsgrad=5)
    figur2 = models.Figur(name="F2", kategorie="Test", schwierigkeitsgrad=6)
    figur3 = models.Figur(name="F3", kategorie="Test", schwierigkeitsgrad=7)
    db.add_all([figur1, figur2, figur3])
    db.commit()

    # Create Anmeldung
    anmeldung = models.Anmeldung(
        kind_id=kind.id,
        wettkampf_id=wettkampf.id,
        startnummer=1,
        anmeldedatum=date.today(),
        vorlaeufig=0,
        status="aktiv"
    )
    db.add(anmeldung)
    db.commit()

    # Act - Add one figur
    updated = repo.add_figur(anmeldung.id, figur1.id)

    # Assert
    assert updated is not None
    assert len(updated.figuren) == 1

    # Act - Set multiple figuren (replaces existing)
    updated2 = repo.set_figuren(anmeldung.id, [figur2.id, figur3.id])

    # Assert
    assert updated2 is not None
    assert len(updated2.figuren) == 2
    figur_names = [f.name for f in updated2.figuren]
    assert "F2" in figur_names
    assert "F3" in figur_names
    assert "F1" not in figur_names  # Should be replaced
