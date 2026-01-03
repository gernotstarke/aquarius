"""
SQLAlchemy models for Aquarius CRUD prototype.
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


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


class Kind(Base):
    """Child model - participant in competitions."""
    __tablename__ = "kind"

    id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False, index=True)
    geburtsdatum = Column(Date, nullable=False)
    geschlecht = Column(String(1))  # M, W, D
    verein = Column(String)
