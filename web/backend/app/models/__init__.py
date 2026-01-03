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
