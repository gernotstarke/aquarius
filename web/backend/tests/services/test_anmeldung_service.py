"""Unit tests for AnmeldungService (Step 5)."""
import pytest
from unittest.mock import Mock
from datetime import date

from app import models
from app.anmeldung import schemas as anmeldung_schemas
# This will cause an ImportError until the service is implemented
from app.anmeldung.services import AnmeldungService

@pytest.fixture
def mock_repos():
    """Fixture to provide mocked repositories."""
    return {
        "anmeldung": Mock(),
        "kind": Mock(),
        "wettkampf": Mock(),
        "figur": Mock(),
    }

def test_create_anmeldung_logic_happy_path(mock_repos):
    """
    Requirement for Step 5:
    Service should coordinate the creation of an Anmeldung.
    """
    # Arrange
    service = AnmeldungService(
        anmeldung_repo=mock_repos["anmeldung"],
        kind_repo=mock_repos["kind"],
        wettkampf_repo=mock_repos["wettkampf"],
        figur_repo=mock_repos["figur"]
    )
    
    # Mock Data
    mock_kind = models.Kind(id=1, versicherung_id=1, verein_id=1) # Insured
    mock_wettkampf = models.Wettkampf(id=1, max_teilnehmer=100)
    mock_repos["kind"].get.return_value = mock_kind
    mock_repos["wettkampf"].get.return_value = mock_wettkampf
    mock_repos["anmeldung"].count_final_registrations.return_value = 50 
    mock_repos["anmeldung"].get_next_startnummer.return_value = 10
    
    # Input
    input_data = anmeldung_schemas.AnmeldungCreate(
        kind_id=1,
        wettkampf_id=1,
        figur_ids=[1, 2]
    )
    
    # Act
    result = service.create_anmeldung(input_data)
    
    # Assert
    assert result.vorlaeufig == 0
    assert result.status == "aktiv"
    mock_repos["anmeldung"].create.assert_called_once()

def test_create_anmeldung_logic_missing_insurance(mock_repos):
    """
    Requirement for Step 5:
    If Kind has no insurance, Anmeldung must be 'vorläufig'.
    """
    # Arrange
    service = AnmeldungService(
        anmeldung_repo=mock_repos["anmeldung"],
        kind_repo=mock_repos["kind"],
        wettkampf_repo=mock_repos["wettkampf"],
        figur_repo=mock_repos["figur"]
    )
    mock_kind = models.Kind(id=1, versicherung_id=None, verein_id=None, verband_id=None) 
    mock_repos["kind"].get.return_value = mock_kind
    mock_repos["wettkampf"].get.return_value = models.Wettkampf(id=1, max_teilnehmer=100)
    mock_repos["anmeldung"].count_final_registrations.return_value = 0
    
    input_data = anmeldung_schemas.AnmeldungCreate(kind_id=1, wettkampf_id=1, figur_ids=[1])
    
    # Act
    result = service.create_anmeldung(input_data)
    
    # Assert
    assert result.vorlaeufig == 1
    assert "keine Versicherung" in str(result.status_reasons) # Assuming we add reasons to the model or log