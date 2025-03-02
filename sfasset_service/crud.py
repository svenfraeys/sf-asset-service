from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

DATA_ROOT = "C:/sfasset_data"
MODEL_SEP = ":"
ENTITY_SEP = "-"
VERSION_SEP = "@"


def rest_error(detail: str) -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(
    db: Session, item: schemas.ItemCreate, user_id: int
) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_spaces(
    db: Session, skip: int = 0, limit: int = 100, code: str = "", name: str = ""
) -> list[models.Space]:
    query = db.query(models.Space)
    if code:
        query = query.filter(models.Space.code == code)
    if name:
        query = query.filter(models.Space.name == name)
    return query.offset(skip).limit(limit).all()


def create_space(
    db: Session, space: schemas.SpaceCreate, code: str = ""
) -> models.Space:
    db_space = models.Space(name=space.name, code=code)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space


def get_space_by_code(db: Session, code: str) -> models.Space | None:
    return db.query(models.Space).filter(models.Space.code == code).first()


def get_entities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    project_id: int = 0,
    parent_id: int = 0,
    code: str = "",
    id: int = 0,
) -> list[models.Entity]:
    query = db.query(models.Entity)
    if name:
        query = query.filter(models.Entity.name == name)
    if project_id:
        query = query.filter(models.Entity.project_id == project_id)
    if parent_id:
        query = query.filter(models.Entity.parent_id == parent_id)
    if code:
        query = query.filter(models.Entity.code == code)
    if id:
        query = query.filter(models.Entity.id == id)

    return query.offset(skip).limit(limit).all()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    code: str = "",
    space_id: int = 0,
) -> list[models.Project]:
    query = db.query(models.Project)
    if name:
        query = query.filter(models.Project.name == name)
    if space_id:
        query = query.filter(models.Project.space_id == space_id)
    if code:
        query = query.filter(models.Project.code == code)

    return query.offset(skip).limit(limit).all()


def get_space_by_id(db: Session, id: int) -> models.Space | None:
    return db.query(models.Space).filter(models.Space.id == id).first()


def get_entity_by_id(db: Session, id: int) -> models.Entity | None:
    return db.query(models.Entity).filter(models.Entity.id == id).first()


def get_project_by_id(db: Session, id: int) -> models.Project | None:
    return db.query(models.Project).filter(models.Project.id == id).first()


def get_entity_by_code(db: Session, code: str) -> models.Entity | None:
    return db.query(models.Entity).filter(models.Entity.code == code).first()


def get_project_by_code(db: Session, code: str) -> models.Project | None:
    return db.query(models.Project).filter(models.Project.code == code).first()


def create_entity(db: Session, entity: schemas.EntityCreate) -> models.Entity:
    db_entity = models.Entity(**entity.model_dump())

    if entity.parent_id:
        parent_entity = get_entity_by_id(db, entity.parent_id)
        if not parent_entity:
            raise rest_error("could not find parent entity")
        code = parent_entity.code + ENTITY_SEP + entity.name
        db_entity.project_id = parent_entity.project_id
    else:
        project = get_project_by_id(db, entity.project_id)
        code = project.code + MODEL_SEP + entity.name

    if get_entity_by_code(db, code):
        raise rest_error("Entity with code already exists")

    if db_entity.parent_id == 0:
        db_entity.parent_id = None

    if db_entity.project_id == 0:
        db_entity.project_id = None

    db_entity.code = str(code)

    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())

    space = get_space_by_id(db, project.space_id)
    if not space:
        raise rest_error("Space not found")
    code = space.code + MODEL_SEP + project.name

    if get_project_by_code(db, code):
        raise rest_error("project with code already exists")

    if db_project.space_id == 0:
        db_project.space_id = None

    db_project.code = code

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_branch_by_id(db: Session, id: int):
    return db.query(models.AssetBranch).filter(models.AssetBranch.id == id).first()


def get_asset_by_id(db: Session, id: int):
    return db.query(models.Asset).filter(models.Asset.id == id).first()


def get_assets(
    db: Session,
    code: str = "",
    entity_id: int = 0,
    project_id: int = 0,
    id: int = 0,
    name: str = "",
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Asset)
    if code:
        query = query.filter(models.Asset.code == code)

    if name:
        query = query.filter(models.Asset.name == name)

    if entity_id:
        query = query.filter(models.Asset.entity_id == entity_id)

    if project_id:
        query = query.filter(models.Asset.project_id == project_id)

    if id:
        query = query.filter(models.Asset.id == id)

    return query.offset(skip).limit(limit).all()


def get_asset_by_code(db: Session, code: str):
    return db.query(models.Asset).filter(models.Asset.code == code).first()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(name=asset.name, entity_id=asset.entity_id)

    entity = get_entity_by_id(db, asset.entity_id)
    if not entity:
        raise rest_error(f"Entity not found with id {asset.entity_id}")

    code = entity.code + MODEL_SEP + asset.name
    if get_asset_by_code(db, str(code)):
        raise rest_error(f"Asset with code {code} already exists")

    db_asset.code = str(code)
    db_asset.project_id = entity.project_id

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    # let s make a default main branch
    db_branch = models.AssetBranch(asset_id=db_asset.id, name="main")
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_asset


def get_asset_version_by_code(db: Session, code: str):
    return (
        db.query(models.AssetVersion).filter(models.AssetVersion.code == code).first()
    )


def get_asset_branches(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_id: int = None,
    id: int = None,
):
    query = db.query(models.AssetBranch)
    if name:
        query = query.filter(models.AssetBranch.name == name)
    if asset_id:
        query = query.filter(models.AssetBranch.asset_id == asset_id)
    if id:
        query = query.filter(models.AssetBranch.id == id)

    return query.offset(skip).limit(limit).all()


def get_asset_tags(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    asset_id: int = 0,
    branch_id: int = 0,
    asset_version_id: int = 0,
    id: int = 0,
):
    query = db.query(models.AssetTag)
    if name:
        query = query.filter(models.AssetTag.name == name)
    if asset_id:
        query = query.filter(models.AssetTag.asset_id == asset_id)
    if id:
        query = query.filter(models.AssetTag.id == id)
    if branch_id:
        query = query.filter(models.AssetTag.branch_id == branch_id)
    if asset_version_id:
        query = query.filter(models.AssetTag.asset_version_id == asset_version_id)
    return query.offset(skip).limit(limit).all()


def get_asset_versions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_id: int = None,
    code: str = None,
    id: int = None,
    branch_id: int = None,
):
    query = db.query(models.AssetVersion)
    if name:
        query = query.filter(models.AssetVersion.name == name)
    if asset_id:
        query = query.filter(models.AssetVersion.asset_id == asset_id)
    if code:
        query = query.filter(models.AssetVersion.code == code)
    if id:
        query = query.filter(models.AssetVersion.id == id)
    if branch_id:
        query = query.filter(models.AssetVersion.branch_id == branch_id)

    return query.offset(skip).limit(limit).all()


def update_asset_version(
    db: Session, asset_version_id: int, asset_version: schemas.AssetVersion
):
    db_asset_version = get_asset_version_by_id(db, asset_version_id)
    if not db_asset_version:
        raise rest_error(detail=f"AssetVersion not found with id {asset_version_id}")

    db_asset_version.locked = asset_version.locked
    db_asset_version.official = asset_version.official
    # for input_id in asset_version.input_ids:
    #     input_asset_version = get_asset_version_by_id(db, input_id)
    #     db_asset_version.inputs.append(input_asset_version)

    db.add(db_asset_version)
    db.commit()
    db.refresh(db_asset_version)
    return db_asset_version


def update_asset_tag(db: Session, asset_tag_id: int, asset_tag: schemas.AssetTag):
    db_asset_tag = get_asset_tag_by_id(db, asset_tag_id)
    if not db_asset_tag:
        raise rest_error(f"AssetTag not found with id {asset_tag_id}")

    db_asset_tag.asset_version_id = asset_tag.asset_version_id
    db.add(db_asset_tag)
    db.commit()
    db.refresh(db_asset_tag)
    return db_asset_tag


def create_asset_branch(db: Session, asset_branch: schemas.AssetBranchCreate):
    assert not get_asset_branches(
        db, asset_id=asset_branch.asset_id, name=asset_branch.name
    )

    asset = get_asset_by_id(db, asset_branch.asset_id)
    assert asset, f"no asset found with id {asset_branch.asset_id}"

    # let s make a default main branch
    db_branch = models.AssetBranch(asset_id=asset.id, name=asset_branch.name)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def create_asset_tag(db: Session, asset_tag: schemas.AssetTagCreate):
    assert not get_asset_tags(
        db,
        asset_id=asset_tag.asset_id,
        name=asset_tag.name,
        branch_id=asset_tag.branch_id,
    )

    asset = get_asset_by_id(db, asset_tag.asset_id)
    assert asset, f"no asset found with id {asset_tag.asset_id}"

    # let s make a default main branch
    db_tag = models.AssetTag(
        asset_id=asset.id,
        name=asset_tag.name,
        branch_id=asset_tag.branch_id,
        asset_version_id=asset_tag.asset_version_id,
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def create_asset_version(db: Session, asset_version: schemas.AssetVersionCreate):
    db_asset_version = models.AssetVersion(**asset_version.dict())

    asset = get_asset_by_id(db, asset_version.asset_id)
    assert asset, f"no asset found with id {asset_version.asset_id}"

    branch = get_branch_by_id(db, asset_version.branch_id)
    assert branch, f"no branch found with id {asset_version.branch_id}"
    branch.version_counter += 1
    db.add(branch)
    db.commit()
    db.refresh(branch)

    version_number = branch.version_counter
    db_asset_version.version = version_number
    name = f"{branch.name}.{version_number}"
    code = f"{asset.code}@{name}"

    if get_asset_version_by_code(db, code):
        raise rest_error(f"AssetVersion with code already exists {code}")

    db_asset_version.branch_id = branch.id
    db_asset_version.code = code
    db_asset_version.message = asset_version.message
    db_asset_version.name = name
    entity_names = []
    entity = get_entity_by_id(db, asset.entity_id)
    project = get_project_by_id(db, entity.project_id)
    space = get_space_by_id(db, project.space_id)

    while entity:
        entity_names.append(entity.name)
        entity = get_entity_by_id(db, entity.parent_id)
    entity_names.reverse()
    entities_dirs = "/".join(entity_names)
    db_asset_version.rel_data_dir = f"{space.code}/{project.name}/{entities_dirs}/{asset.name}/{branch.name}.{version_number}"
    db_asset_version.data_dir = DATA_ROOT + "/" + db_asset_version.rel_data_dir

    db.add(db_asset_version)
    db.commit()
    db.refresh(db_asset_version)
    return db_asset_version


def get_asset_files(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_version_id: int = None,
):
    query = db.query(models.AssetFile)
    if name:
        query = query.filter(models.AssetFile.name == name)
    if asset_version_id:
        query = query.filter(models.AssetFile.asset_version_id == asset_version_id)
    return query.offset(skip).limit(limit).all()


def get_asset_version_by_id(db: Session, id: int):
    return db.query(models.AssetVersion).filter(models.AssetVersion.id == id).first()


def get_asset_tag_by_id(db: Session, id: int):
    return db.query(models.AssetTag).filter(models.AssetTag.id == id).first()


def create_asset_file(db: Session, asset_file: schemas.AssetFileCreate):
    asset_version = get_asset_version_by_id(db, asset_file.asset_version_id)
    if not asset_version:
        raise rest_error(
            f"could not find asset version with id {asset_file.asset_version_id}"
        )
    db_asset_file = models.AssetFile()
    db_asset_file.name = asset_file.name
    db_asset_file.asset_version_id = asset_version.id

    db.add(db_asset_file)
    db.commit()
    db.refresh(db_asset_file)
    return db_asset_file


def get_asset_links(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    id: int = 0,
    asset_version_id: int = None,
    target_asset_version_id: int = None,
):
    query = db.query(models.AssetLink)
    if name:
        query = query.filter(models.AssetLink.name == name)
    if asset_version_id:
        query = query.filter(models.AssetLink.asset_version_id == asset_version_id)
    if target_asset_version_id:
        query = query.filter(
            models.AssetLink.target_asset_version_id == target_asset_version_id
        )

    if id:
        query = query.filter(models.AssetLink.id == id)

    return query.offset(skip).limit(limit).all()


def create_asset_link(db: Session, asset_link: schemas.AssetLinkCreate):
    asset_version = get_asset_version_by_id(db, asset_link.asset_version_id)
    if not asset_version:
        raise rest_error("could not find asset version")

    db_asset_link = models.AssetLink(**asset_link.dict())
    db.add(db_asset_link)
    db.commit()
    db.refresh(db_asset_link)
    return db_asset_link
