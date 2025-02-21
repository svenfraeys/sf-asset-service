from pydantic import BaseModel
from typing import Union
from typing import Optional


class SpaceBase(BaseModel):
    name: str


class Space(SpaceBase):
    id: int
    code: str


class SpaceCreate(SpaceBase):
    pass


class ProjectBase(BaseModel):
    name: str
    space_id: int


class Project(ProjectBase):
    id: int
    code: str


class ProjectCreate(ProjectBase):
    pass


class EntityBase(BaseModel):
    name: str
    project_id: int
    parent_id: Union[int, None] = None


class Entity(EntityBase):
    id: int
    code: str


class EntityCreate(EntityBase):
    pass


class AssetBase(BaseModel):
    name: str
    entity_id: int


class Asset(AssetBase):
    id: int
    code: str
    project_id: int


class AssetCreate(AssetBase):
    pass


class AssetBranchBase(BaseModel):
    asset_id: int
    name: str


class AssetBranch(AssetBranchBase):
    id: int
    version_counter: int


class AssetBranchCreate(AssetBranchBase):
    pass


class AssetTagBase(BaseModel):
    asset_id: int
    asset_version_id: int
    branch_id: int
    name: str


class AssetTag(AssetTagBase):
    id: int


class AssetTagCreate(AssetTagBase):
    pass


class AssetVersionBase(BaseModel):
    asset_id: int
    message: str
    branch_id: int


class AssetVersion(AssetVersionBase):
    id: int
    code: str
    name: str
    data_dir: str
    rel_data_dir: str
    locked: bool
    official: bool


class AssetVersionCreate(AssetVersionBase):
    pass


class AssetFileBase(BaseModel):
    asset_version_id: int
    name: str


class AssetFile(AssetFileBase):
    id: int


class AssetFileCreate(AssetFileBase):
    pass


class AssetLinkBase(BaseModel):
    asset_version_id: int
    target_asset_version_id: Optional[int] = None
    name: str
    dependency: bool
    output: bool


class AssetLink(AssetLinkBase):
    id: int


class AssetLinkCreate(AssetLinkBase):
    pass


class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    first_name: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
