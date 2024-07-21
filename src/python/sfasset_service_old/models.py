from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship
from .db import engine

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)


class Space(Base):
    __tablename__ = "spaces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    entities = relationship("Entity", back_populates="space")
    code = Column(String)


class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    space_id = Column(Integer, ForeignKey("spaces.id"))
    space = relationship("Space", back_populates="entities")
    streams = relationship("Stream", back_populates="entity")
    code = Column(String)


class Stream(Base):
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    entity = relationship("Entity", back_populates="streams")
    assets = relationship("Asset", back_populates="stream")
    version_counter = Column(Integer, default=0)
    code = Column(String)


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(Integer)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    stream = relationship("Stream", back_populates="assets")
    attrs = relationship("Attr", back_populates="asset")
    files = relationship("File", back_populates="asset")
    path = Column(String)
    type_id = Column(Integer, ForeignKey("asset_types.id"))
    type = relationship("AssetType", back_populates="assets")
    code = Column(String)


class AssetType(Base):
    __tablename__ = "asset_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    assets = relationship("Asset", back_populates="type")


class Attr(Base):
    __tablename__ = "attrs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value_str = Column(String)
    value_int = Column(Integer)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="attrs")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="files")
