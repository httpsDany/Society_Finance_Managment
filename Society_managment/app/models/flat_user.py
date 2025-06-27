from sqlalchemy import Column, Integer, String, Enum, Date, Text,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import enum

# --- Enum Definitions ---
class RoleEnum(str, enum.Enum):
    admin = "admin"
    owner = "rowner"
    renter = "renter"

class FlatStatusEnum(str, enum.Enum):
    empty = "empty"
    owned = "owned"
    rented = "rented"

# --- User Model ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    password_hash = Column(Text, nullable=True)
    oauth_provider = Column(String(50), nullable=True)
    oauth_id = Column(String(100), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.renter)

    flat_building_no = Column(Integer, nullable=True, index=True)
    flat_no = Column(String(10), nullable=True)
    building_no = Column(Integer, nullable=True)  # For compatibility if needed

# --- Flat Model ---
class Flat(Base):
    __tablename__ = "flats"

    building_no = Column(Integer, primary_key=True)
    flat_no = Column(String(10), primary_key=True)

    flat_type = Column(String(20), nullable=True)
    status = Column(Enum(FlatStatusEnum), default=FlatStatusEnum.empty)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    due_amt = Column(Integer, nullable=True)
    fine = Column(Integer, default=0)
    miscellaneous = Column(Integer, default=0)
    maintenance_fee = Column(Integer, nullable=True)
    total_due = Column(Integer, nullable=True)

#---Buildings---
class Building(Base):
    __tablename__ = "buildings"

    building_no = Column(Integer, primary_key=True, autoincrement=True)
    building_name = Column(String(100), nullable=False)
    floors = Column(Integer, nullable=False)
    flats_per_floor = Column(Integer, nullable=False)

# --- FlatType Model ---
class FlatType(Base):
    __tablename__ = "flat_types"

    type_name = Column(String(20), primary_key=True)
    maintenance_fee = Column(Integer, nullable=False)
    rent= Column(Integer, nullable=True)

# --- Flat Type Mapping ---
class FlatTypeMapping(Base):
    __tablename__ = "flat_type_mappings"

    building_no = Column(Integer, primary_key=True)
    flat_no = Column(String(10), primary_key=True)
    flat_type = Column(String(20), ForeignKey("flat_types.type_name"), nullable=False)
