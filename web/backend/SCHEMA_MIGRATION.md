# Schema Migration - Step 2: Modularize Schemas

## Overview

As part of the DDD migration, all Pydantic schemas have been moved from the central `app/schemas/__init__.py` to domain-specific modules while maintaining full backward compatibility.

## Schema Organization

### Domain Structure

```
app/
├── grunddaten/
│   └── schemas.py      # Master data: Saison, Schwimmbad, Verein, Verband, Versicherung, Figur
├── kind/
│   └── schemas.py      # Kind (Child) schemas
├── wettkampf/
│   └── schemas.py      # Wettkampf (Competition) schemas
├── anmeldung/
│   └── schemas.py      # Anmeldung (Registration) schemas
└── schemas/
    └── __init__.py     # Re-exports all schemas for backward compatibility
```

### Schema Dependencies

```
Grunddaten (independent)
    ↓
Kind (depends on: Verein, Verband, Versicherung from Grunddaten)
    ↓
Anmeldung (depends on: Kind, Figur from Grunddaten)
    ↓
WettkampfWithDetails (depends on: Anmeldung, Figur, Saison, Schwimmbad)
```

## Circular Dependency Workaround

### Problem

Pydantic schemas with cross-domain relationships created potential circular import issues:
- `Kind` references `Verein`, `Verband`, `Versicherung` (from Grunddaten)
- `Anmeldung` references `Kind` and `Figur`
- `WettkampfWithDetails` references `Anmeldung`, `Figur`, etc.

### Solution: TYPE_CHECKING + model_rebuild()

We used Python's `TYPE_CHECKING` constant combined with Pydantic's `model_rebuild()` method:

#### 1. Use TYPE_CHECKING for forward references

Example in `app/kind/schemas.py`:

```python
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.grunddaten.schemas import Verein, Verband, Versicherung

class Kind(KindBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    verein: Optional["Verein"] = None  # String quotes for forward reference
    verband: Optional["Verband"] = None
    versicherung: Optional["Versicherung"] = None
```

**Why this works:**
- `TYPE_CHECKING` is `False` at runtime, so imports don't execute
- `True` only for type checkers (mypy, pyright)
- Quoted type hints become forward references

#### 2. Call model_rebuild() after all imports

In `app/schemas/__init__.py` (after importing all schemas):

```python
# Resolve forward references now that all schemas are imported
Kind.model_rebuild()
Anmeldung.model_rebuild()
WettkampfWithDetails.model_rebuild()
```

**Why this is necessary:**
- Pydantic needs concrete class references to build validators
- `model_rebuild()` resolves forward references after imports complete
- Called once during module initialization, no runtime cost

## Backward Compatibility

The central `app/schemas/__init__.py` re-exports ALL schemas:

```python
from app.grunddaten.schemas import Saison, Schwimmbad, Verein, ...
from app.kind.schemas import Kind, KindCreate, ...
from app.wettkampf.schemas import Wettkampf, ...
from app.anmeldung.schemas import Anmeldung, ...
```

**Result:** Existing code continues to work unchanged:
```python
from app import schemas

# All of these still work:
schemas.Kind
schemas.Anmeldung
schemas.Wettkampf
schemas.Saison
# etc.
```

## Test Results

✅ All 38 backend tests pass  
✅ API response models remain identical  
✅ No breaking changes to existing code  

## Next Steps (Step 3)

- Move domain logic into service/repository layers
- Create domain aggregates
- Implement business rules in aggregate classes
- Further decouple domains

## References

- Issue: #34 - DDD Migration Step 2
- Pydantic docs: https://docs.pydantic.dev/latest/concepts/models/#rebuilding-model-schema
- Python TYPE_CHECKING: https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
