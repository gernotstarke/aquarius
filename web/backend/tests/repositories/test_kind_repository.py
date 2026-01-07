"""Integration tests for KindRepository (Step 4)."""
import pytest
from datetime import date
from sqlalchemy.orm import Session

from app.kind.repository import KindRepository
from app.kind import schemas as kind_schemas
from app import models


def test_kind_repository_create_and_get(db: Session):
    """
    Requirement for Step 4:
    Repo should handle creation and retrieval by ID.
    """
    # Arrange
    repo = KindRepository(db)
    kind_data = kind_schemas.KindCreate(
        vorname="Max",
        nachname="RepoTest",
        geburtsdatum=date(2015, 5, 10),
        geschlecht="M"
    )

    # Act
    created = repo.create(kind_data)
    fetched = repo.get(created.id)

    # Assert
    assert fetched is not None
    assert fetched.vorname == "Max"
    assert fetched.nachname == "RepoTest"
    assert fetched.geburtsdatum == date(2015, 5, 10)
    assert fetched.geschlecht == "M"


def test_kind_repository_search(db: Session):
    """
    Requirement for Step 4:
    Repo should encapsulate the complex search logic currently in router.
    """
    # Arrange
    repo = KindRepository(db)

    # Create test data
    kind1 = kind_schemas.KindCreate(
        vorname="Max",
        nachname="Mustermann",
        geburtsdatum=date(2015, 3, 15),
        geschlecht="M"
    )
    kind2 = kind_schemas.KindCreate(
        vorname="Erika",
        nachname="Musterfrau",
        geburtsdatum=date(2014, 7, 20),
        geschlecht="W"
    )
    kind3 = kind_schemas.KindCreate(
        vorname="Anna",
        nachname="Schmidt",
        geburtsdatum=date(2016, 1, 10),
        geschlecht="W"
    )

    repo.create(kind1)
    repo.create(kind2)
    repo.create(kind3)

    # Act - Search by partial name match
    results, total = repo.search(query="Muster")

    # Assert
    assert total == 2
    assert len(results) == 2
    # Results should include both Mustermann and Musterfrau
    names = [f"{k.vorname} {k.nachname}" for k in results]
    assert "Max Mustermann" in names
    assert "Erika Musterfrau" in names

    # Act - Search with no query (should return all)
    all_results, all_total = repo.search()

    # Assert
    assert all_total >= 3  # At least our 3 test records


def test_kind_repository_search_with_sorting(db: Session):
    """Test that repository handles sorting correctly."""
    # Arrange
    repo = KindRepository(db)

    kind1 = kind_schemas.KindCreate(
        vorname="Zebra",
        nachname="Aardvark",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    kind2 = kind_schemas.KindCreate(
        vorname="Alpha",
        nachname="Beta",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="W"
    )

    repo.create(kind1)
    repo.create(kind2)

    # Act - Sort by nachname ascending (default)
    results_asc, _ = repo.search(sort_by="nachname", sort_order="asc")

    # Assert - Aardvark should come before Beta
    assert results_asc[0].nachname == "Aardvark"
    assert results_asc[1].nachname == "Beta"

    # Act - Sort by vorname descending
    results_desc, _ = repo.search(sort_by="vorname", sort_order="desc", limit=100)

    # Assert - Zebra should come before Alpha
    assert results_desc[0].vorname == "Zebra"


def test_kind_repository_update_and_delete(db: Session):
    """Test update and delete operations."""
    # Arrange
    repo = KindRepository(db)
    kind_data = kind_schemas.KindCreate(
        vorname="Test",
        nachname="Delete",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    created = repo.create(kind_data)

    # Act - Update
    update_data = kind_schemas.KindUpdate(
        vorname="Updated",
        nachname="Name",
        geburtsdatum=date(2015, 1, 1),
        geschlecht="M"
    )
    updated = repo.update(created.id, update_data)

    # Assert
    assert updated is not None
    assert updated.vorname == "Updated"
    assert updated.nachname == "Name"

    # Act - Delete
    deleted = repo.delete(created.id)
    fetched = repo.get(created.id)

    # Assert
    assert deleted is True
    assert fetched is None
