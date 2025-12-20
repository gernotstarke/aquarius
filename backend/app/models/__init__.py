"""
SQLAlchemy models for Arqua42 CRUD prototype.
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for Wettkampf <-> Figuren (many-to-many)
wettkampf_figuren = Table(
    'wettkampf_figuren',
    Base.metadata,
    Column('wettkampf_id', Integer, ForeignKey('wettkampf.id'), primary_key=True),
    Column('figur_id', Integer, ForeignKey('figur.id'), primary_key=True)
)

# Association table for Anmeldung <-> Figuren (many-to-many)
anmeldung_figuren = Table(
    'anmeldung_figuren',
    Base.metadata,
    Column('anmeldung_id', Integer, ForeignKey('anmeldung.id'), primary_key=True),
    Column('figur_id', Integer, ForeignKey('figur.id'), primary_key=True)
)


class Saison(Base):
    """Season model - represents a competition season."""
    __tablename__ = "saison"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)

    # Relationships
    wettkämpfe = relationship("Wettkampf", back_populates="saison")


class Schwimmbad(Base):
    """Pool/Swimming facility model."""
    __tablename__ = "schwimmbad"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    adresse = Column(String, nullable=False)
    phone_no = Column(String)
    manager = Column(String)

    # Relationships
    wettkämpfe = relationship("Wettkampf", back_populates="schwimmbad")


class Wettkampf(Base):
    """Competition model."""
    __tablename__ = "wettkampf"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    datum = Column(Date, nullable=False)
    max_teilnehmer = Column(Integer)
    saison_id = Column(Integer, ForeignKey("saison.id"), nullable=False)
    schwimmbad_id = Column(Integer, ForeignKey("schwimmbad.id"), nullable=False)

    # Relationships
    saison = relationship("Saison", back_populates="wettkämpfe")
    schwimmbad = relationship("Schwimmbad", back_populates="wettkämpfe")
    figuren = relationship("Figur", secondary=wettkampf_figuren, back_populates="wettkämpfe")
    anmeldungen = relationship("Anmeldung", back_populates="wettkampf")


class Kind(Base):
    """Child model - participant in competitions."""
    __tablename__ = "kind"

    id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False, index=True)
    geburtsdatum = Column(Date, nullable=False)
    geschlecht = Column(String(1))  # M, W, D
    verein = Column(String)

    # Relationships
    anmeldungen = relationship("Anmeldung", back_populates="kind")


class Figur(Base):
    """Swimming figure/trick model."""
    __tablename__ = "figur"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # Removed unique constraint - same figure can be in multiple categories
    beschreibung = Column(Text)
    schwierigkeitsgrad = Column(Integer)  # 1-5 (stored as int, e.g. 12 for 1.2)
    kategorie = Column(String)  # z.B. "Ballettbein", "Vertikale", "Flamingo"
    min_alter = Column(Integer)  # Mindestalter für diese Figur
    bild = Column(String)  # Pfad zum Bild (optional)

    # Relationships
    wettkämpfe = relationship("Wettkampf", secondary=wettkampf_figuren, back_populates="figuren")


class Anmeldung(Base):
    """Registration model - links Kind to Wettkampf with selected Figuren."""
    __tablename__ = "anmeldung"

    id = Column(Integer, primary_key=True, index=True)
    kind_id = Column(Integer, ForeignKey("kind.id"), nullable=False)
    wettkampf_id = Column(Integer, ForeignKey("wettkampf.id"), nullable=False)
    anmeldedatum = Column(Date, nullable=False)
    status = Column(String, default="aktiv")  # aktiv, storniert

    # Relationships
    kind = relationship("Kind", back_populates="anmeldungen")
    wettkampf = relationship("Wettkampf", back_populates="anmeldungen")
    figuren = relationship("Figur", secondary=anmeldung_figuren)
