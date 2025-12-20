# ADR-007: Alembic für Datenbank-Migrationen

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Datenbank-Schemas ändern sich während der Entwicklung und im Produktivbetrieb. Wir benötigen ein Migrations-System für versionierte, nachvollziehbare Schema-Änderungen.

## Entscheidung

Wir verwenden **Alembic** als Datenbank-Migrations-Tool in Kombination mit SQLAlchemy.

## Begründung

### Vorteile

- **SQLAlchemy-Integration** - Offizielles Migrations-Tool von SQLAlchemy
- **Autogenerate** - Migrationen aus SQLAlchemy Models generieren
- **Versionskontrolle** - Migrations-History im Git-Repository
- **Rollback-Support** - Upgrade/Downgrade zwischen Versionen
- **Team-fähig** - Merge-Konflikte bei Migrations-Files lösbar
- **Branching** - Multiple Entwicklungszweige möglich
- **Turso-kompatibel** - Funktioniert mit SQLite/libSQL

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Manuelles SQL** | Fehleranfällig, nicht versioniert |
| **Django Migrations** | Benötigt Django Framework |
| **Flyway** | Java-basiert, Overkill |
| **Liquibase** | XML-basiert, Java-lastig |
| **Yoyo** | Kleinere Community, weniger Features |

## Konsequenzen

### Positiv

- Schema-Änderungen sind nachvollziehbar und reproduzierbar
- Automatische Migration beim Deployment
- Einfaches Rollback bei Problemen
- Lokale Entwicklung mit identischem Schema

### Negativ

- Manuelle Anpassungen bei komplexen Migrationen erforderlich
- Autogenerate erkennt nicht alle Änderungen (Data-Migrations)
- Merge-Konflikte bei parallelen Schema-Änderungen möglich

## Technische Details

```bash
# Migration erstellen
alembic revision --autogenerate -m "add enrollment table"

# Migration ausführen
alembic upgrade head

# Rollback
alembic downgrade -1

# Migration-Status
alembic current
alembic history
```

**Migration File Beispiel:**
```python
"""add enrollment table

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2025-12-17 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = 'abc123def456'
down_revision = 'previous_revision'

def upgrade() -> None:
    op.create_table(
        'anmeldung',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kind_id', sa.Integer(), nullable=False),
        sa.Column('wettkampf_id', sa.Integer(), nullable=False),
        sa.Column('startnummer', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['kind_id'], ['kind.id']),
        sa.ForeignKeyConstraint(['wettkampf_id'], ['wettkampf.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('anmeldung')
```

**Dependencies:**
```json
{
  "alembic": "^1.13.0"
}
```

## CI/CD Integration

```yaml
# GitHub Actions
- name: Run migrations
  run: alembic upgrade head
```

## Deployment-Workflow

1. Entwicklung: Lokale Migrations mit `alembic upgrade head`
2. Git: Migrations-Files committen
3. CI: Automatischer Migrations-Test
4. Production: Migrations vor App-Deployment ausführen
