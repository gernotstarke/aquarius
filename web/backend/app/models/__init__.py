"""
SQLAlchemy models for Aquarius CRUD prototype.
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.database import Base
from .user import User

# Association table for Wettkampf <-> Figur
wettkampf_figur_association = Table(
    'wettkampf_figuren',
    Base.metadata,
    Column('wettkampf_id', Integer, ForeignKey('wettkampf.id'), primary_key=True),
    Column('figur_id', Integer, ForeignKey('figur.id'), primary_key=True)
)

# Association table for Anmeldung <-> Figur
anmeldung_figur_association = Table(
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


class Verein(Base):
    """Club/Association model."""
    __tablename__ = "verein"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    ort = Column(String, nullable=False)
    register_id = Column(String, nullable=False)
    contact = Column(String, nullable=False)

    # Relationships
    kinder = relationship("Kind", back_populates="verein")


class Verband(Base):
    """Association model - a nominating association for children."""
    __tablename__ = "verband"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    abkuerzung = Column(String(5), nullable=False, unique=True, index=True)
    land = Column(String, nullable=False)
    ort = Column(String, nullable=False)

    # Relationships
    kinder = relationship("Kind", back_populates="verband")


class Versicherung(Base):
    """Insurance company model."""
    __tablename__ = "versicherung"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    kurz = Column(String(5), nullable=False, unique=True, index=True)
    land = Column(String, nullable=False)
    hauptsitz = Column(String, nullable=False)

    # Relationships
    kinder = relationship("Kind", back_populates="versicherung")


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
    figuren = relationship("Figur", secondary=wettkampf_figur_association)
    anmeldungen = relationship("Anmeldung", back_populates="wettkampf", cascade="all, delete-orphan")


class Kind(Base):
    """Child model - participant in competitions."""
    __tablename__ = "kind"

    id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False, index=True)
    geburtsdatum = Column(Date, nullable=False)
    geschlecht = Column(String(1))  # M, W, D
    verein_id = Column(Integer, ForeignKey("verein.id"), nullable=True)
    verband_id = Column(Integer, ForeignKey("verband.id"), nullable=True)
    versicherung_id = Column(Integer, ForeignKey("versicherung.id"), nullable=True)
    vertrag = Column(String, nullable=True)

    # Relationships
    verein = relationship("Verein", back_populates="kinder")
    verband = relationship("Verband", back_populates="kinder")
    versicherung = relationship("Versicherung", back_populates="kinder")
    anmeldungen = relationship("Anmeldung", back_populates="kind")


class Figur(Base):
    """Figure model - synchronized swimming figures."""
    __tablename__ = "figur"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    kategorie = Column(String)
    beschreibung = Column(String)
    schwierigkeitsgrad = Column(Integer) # scaled by 10 or float? Usually float, but let's see usage
    altersklasse = Column(String)
    bild = Column(String) # Path to image


class Anmeldung(Base):
    """Registration model."""
    __tablename__ = "anmeldung"

    id = Column(Integer, primary_key=True, index=True)
    kind_id = Column(Integer, ForeignKey("kind.id"), nullable=False)
    wettkampf_id = Column(Integer, ForeignKey("wettkampf.id"), nullable=False)
    startnummer = Column(Integer)
    anmeldedatum = Column(Date, default=date.today)
    vorlaeufig = Column(Integer, default=0) # Boolean as int for SQLite compatibility
    status = Column(String, default="aktiv")

    # Relationships
    kind = relationship("Kind", back_populates="anmeldungen")
    wettkampf = relationship("Wettkampf", back_populates="anmeldungen")
    figuren = relationship("Figur", secondary=anmeldung_figur_association)

# Placeholder for future Domain-Driven Models
# from app.kind import models as kind_models
# from app.anmeldung import models as anmeldung_models
# from app.wettkampf import models as wettkampf_models
# from app.grunddaten import models as grunddaten_models
