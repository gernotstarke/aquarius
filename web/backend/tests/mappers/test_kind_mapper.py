"""Unit tests for Kind Mapper (Step 6)."""
from datetime import date
from unittest.mock import Mock
from app import models

# In Step 6, you will implement this module
# from app.kind.mappers import to_kind_dto

def test_kind_entity_to_dto_mapping():
    """
    Requirement for Step 6:
    Mapper should convert SQLAlchemy Kind entity to Pydantic Kind DTO.
    """
    # Arrange
    # db_kind = models.Kind(
    #     id=1,
    #     vorname="Max",
    #     nachname="Mapper",
    #     geburtsdatum=date(2015, 1, 1),
    #     geschlecht="M",
    #     verein_id=10
    # )
    
    # Act
    # dto = to_kind_dto(db_kind)
    
    # Assert
    # assert dto.id == 1
    # assert dto.vorname == "Max"
    # assert dto.nachname == "Mapper"
    # assert dto.verein_id == 10
    pass

def test_kind_mapper_handles_relationships():
    """
    Requirement for Step 6:
    Mapper should correctly handle nested relationships (e.g. Verein object)
    if they are loaded on the entity.
    """
    # Arrange
    # db_verein = models.Verein(id=10, name="Test Club")
    # db_kind = models.Kind(id=1, verein=db_verein)
    
    # Act
    # dto = to_kind_dto(db_kind)
    
    # Assert
    # assert dto.verein is not None
    # assert dto.verein.name == "Test Club"
    pass
