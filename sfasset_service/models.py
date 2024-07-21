from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Space(Base):
    __tablename__ = "spaces"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    entities = relationship("Entity", back_populates="space")


class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"))
    space = relationship("Space", back_populates="entities")
    parent_id = Column(Integer, ForeignKey("entities.id"))
    parent = relationship("Entity", remote_side=[id])
    children = relationship("Entity", remote_side=[parent_id], uselist=True)
    assets = relationship("Asset", back_populates="entity")


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    entity = relationship("Entity", back_populates="assets")
    asset_versions = relationship("AssetVersion", back_populates="asset")
    data_dir = Column(String)


class AssetVersion(Base):
    __tablename__ = "asset_versions"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="asset_versions")
    data_dir = Column(String, default="")
    rel_data_dir = Column(String, default="")

    asset_files = relationship("AssetFile", back_populates="asset_version")


class AssetFile(Base):
    __tablename__ = "asset_files"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    asset_version_id = Column(Integer, ForeignKey("asset_versions.id"))
    asset_version = relationship("AssetVersion", back_populates="asset_files")
    path = Column(String, default="")
    rel_path = Column(String, default="")
