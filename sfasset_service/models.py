from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base
from typing import List
from sqlalchemy.orm import Mapped


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    entities = relationship("Entity", back_populates="project")
    assets = relationship("Asset", back_populates="project")


class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="entities")
    parent_id = Column(Integer, ForeignKey("entities.id"))
    parent = relationship("Entity", remote_side=[id], backref="children")
    # children = relationship("Entity", remote_side=[parent_id], uselist=True)
    assets = relationship("Asset", back_populates="entity")


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    entity = relationship("Entity", back_populates="assets")
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="assets")

    asset_versions = relationship("AssetVersion", back_populates="asset")
    branches = relationship("AssetBranch", back_populates="asset")
    tags = relationship("AssetTag", back_populates="asset")

    data_dir = Column(String)


class AssetBranch(Base):
    __tablename__ = "asset_branches"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="branches")
    version_counter = Column(Integer, default=0)

    asset_versions = relationship("AssetVersion", back_populates="branch")

    tags = relationship("AssetTag", back_populates="branch")


asset_version_inputs_table = Table(
    "asset_version_inputs",
    Base.metadata,
    Column("asset_version_id", ForeignKey("asset_versions.id")),
    Column("input_asset_version_id", ForeignKey("asset_versions.id")),
)

version_tag_association = Table(
    "asset_asset_tag",
    Base.metadata,
    Column("asset_version_id", Integer, ForeignKey("asset_versions.id")),
    Column("asset_tag_id", Integer, ForeignKey("asset_tags.id")),
)


class AssetVersion(Base):
    __tablename__ = "asset_versions"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="asset_versions")

    branch_id = Column(Integer, ForeignKey("asset_branches.id"))
    branch = relationship("AssetBranch", back_populates="asset_versions")

    data_dir = Column(String, default="")
    rel_data_dir = Column(String, default="")
    message = Column(String, default="")

    tags = relationship(
        "AssetTag",
        secondary=version_tag_association,
        back_populates="asset_versions",
    )

    asset_files = relationship("AssetFile", back_populates="asset_version")
    asset_links = relationship(
        "AssetLink",
        back_populates="asset_version",
        foreign_keys="[AssetLink.asset_version_id]",
    )
    source_asset_links = relationship(
        "AssetLink",
        back_populates="asset_version",
        foreign_keys="[AssetLink.target_asset_version_id]",
    )

    locked = Column(Boolean, default=False)
    official = Column(Boolean, default=False)
    # inputs: Mapped[List["AssetVersion"]] = relationship(
    #     secondary=asset_version_inputs_table, foreign_keys="input_asset_version_id"
    # )
    inputs = relationship(
        "AssetVersion",
        secondary=asset_version_inputs_table,
        primaryjoin=id == asset_version_inputs_table.c.asset_version_id,
        secondaryjoin=id == asset_version_inputs_table.c.input_asset_version_id,
        # backref="related_to",
    )


class AssetTag(Base):
    __tablename__ = "asset_tags"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="tags")
    asset_version_id = Column(Integer, ForeignKey("asset_versions.id"))
    asset_version = relationship(
        "AssetVersion", back_populates="tags", foreign_keys=[asset_version_id]
    )
    branch_id = Column(Integer, ForeignKey("asset_branches.id"))
    branch = relationship("AssetBranch", back_populates="tags")

    asset_versions = relationship(
        "AssetVersion", secondary=version_tag_association, back_populates="tags"
    )


class AssetLink(Base):
    __tablename__ = "asset_links"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    asset_version_id = Column(Integer, ForeignKey("asset_versions.id"))
    asset_version = relationship(
        "AssetVersion", back_populates="asset_links", foreign_keys=[asset_version_id]
    )

    target_asset_version_id = Column(
        Integer, ForeignKey("asset_versions.id"), default=None
    )
    target_asset_version = relationship(
        "AssetVersion",
        back_populates="source_asset_links",
        foreign_keys=[target_asset_version_id],
    )

    dependency = Column(Boolean, default=False)
    output = Column(Boolean, default=False)


class AssetFile(Base):
    __tablename__ = "asset_files"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    asset_version_id = Column(Integer, ForeignKey("asset_versions.id"))
    asset_version = relationship("AssetVersion", back_populates="asset_files")

    # TODO: remove these
    path = Column(String, default="")
    rel_path = Column(String, default="")
